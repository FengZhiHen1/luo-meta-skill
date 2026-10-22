#!/usr/bin/env python3
"""Aggregate a benchmark iteration into benchmark.json and benchmark.md.

Reads <iteration>/eval-*/{with_skill,old_skill,without_skill}/{grading.json,timing.json},
validates each grading file against schemas/results.schema.json, and reports the
with-skill gain over the baseline.

Standard library only.

Usage:
    python summarize_runs.py ITERATION_DIR --skill-name NAME [--case-file FILE] [--out DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_SCHEMA = SCRIPT_DIR.parent / "schemas" / "results.schema.json"
WITH_SKILL = "with_skill"
BASELINE_ORDER = ("old_skill", "without_skill")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_grading(grading, schema, label, errors):
    """Validate one grading file against the 'grading' definition of the results schema."""
    definitions = schema.get("$defs", {})
    grading_schema = dict(definitions.get("grading", {}))
    root = {"$defs": definitions}

    def resolve(value, node, path):
        if "$ref" in node:
            ref = node["$ref"]
            target = root
            for part in ref[2:].split("/"):
                target = target[part]
            return resolve(value, target, path)
        if "type" in node:
            expected = node["type"] if isinstance(node["type"], list) else [node["type"]]
            ok = any(
                isinstance(value, {"object": dict, "array": list, "string": str,
                                   "boolean": bool, "number": (int, float)}.get(item, object))
                and not (item in ("number", "integer") and isinstance(value, bool))
                for item in expected
            )
            if not ok:
                errors.append(label + " " + path + ": expected " + "/".join(expected))
                return
        if isinstance(value, dict):
            for key in node.get("required", []):
                if key not in value:
                    errors.append(label + " " + path + ": missing field " + key)
            for key, sub in node.get("properties", {}).items():
                if key in value:
                    resolve(value[key], sub, path + "." + key)
        if isinstance(value, list) and isinstance(node.get("items"), dict):
            for index, item in enumerate(value):
                resolve(item, node["items"], path + "[" + str(index) + "]")

    resolve(grading, grading_schema, "$")


def read_run(run_dir, schema, errors):
    record = {"pass_rate": None, "passed": 0, "failed": 0, "total": 0}
    grading_path = run_dir / "grading.json"
    if not grading_path.exists():
        return None
    try:
        grading = load_json(grading_path)
    except json.JSONDecodeError as exc:
        errors.append(str(grading_path) + ": invalid JSON: " + str(exc))
        return None
    before = len(errors)
    check_grading(grading, schema, str(grading_path), errors)
    if len(errors) > before:
        return None
    summary = grading.get("summary", {})
    record["passed"] = summary.get("passed", 0)
    record["failed"] = summary.get("failed", 0)
    record["total"] = summary.get("total", len(grading.get("assertions", [])))
    pass_rate = summary.get("pass_rate")
    if pass_rate is None:
        total = record["total"] or 1
        pass_rate = record["passed"] / total
    record["pass_rate"] = round(float(pass_rate), 3)
    if record["total"] and record["total"] != len(grading.get("assertions", [])):
        print("WARN: " + str(grading_path) + ": summary.total disagrees with the assertion count; "
              "the file may still be mid-write, so re-run the aggregation")
    record["assertions"] = [
        {"text": item.get("text"), "passed": item.get("passed")}
        for item in grading.get("assertions", []) if isinstance(item, dict)
    ]
    feedback = grading.get("assertion_feedback")
    if feedback:
        record["assertion_feedback"] = feedback

    timing_path = run_dir / "timing.json"
    if timing_path.exists():
        try:
            timing = load_json(timing_path)
            if isinstance(timing.get("total_tokens"), (int, float)):
                record["tokens"] = timing["total_tokens"]
            if isinstance(timing.get("duration_ms"), (int, float)):
                record["duration_ms"] = timing["duration_ms"]
        except json.JSONDecodeError as exc:
            errors.append(str(timing_path) + ": invalid JSON: " + str(exc))
    return record


def collect_runs(config_dir, schema, errors):
    """Read one grading.json from the config directory, or average the run-*/ repetitions inside it."""
    single = config_dir / "grading.json"
    if single.exists():
        record = read_run(config_dir, schema, errors)
        return [record] if record else []
    attempts = []
    for sub in sorted(item for item in config_dir.iterdir() if item.is_dir() and item.name.startswith("run-")):
        record = read_run(sub, schema, errors)
        if record:
            attempts.append(record)
    return attempts


def merge_assertions(attempts):
    """An assertion counts as passed only when every repetition passed it."""
    verdicts = {}
    for attempt in attempts:
        for item in attempt.get("assertions", []):
            text = item.get("text")
            if text is None:
                continue
            verdicts.setdefault(text, []).append(item.get("passed") is True)
    return [{"text": text, "passed": all(values)} for text, values in verdicts.items()]


def weighted_pass_rate(cases, configuration):
    weighted = 0.0
    total_weight = 0.0
    counted = 0
    for case in cases:
        run = case["configurations"].get(configuration)
        if not run or run.get("pass_rate") is None:
            continue
        weight = float(case.get("weight", 1))
        weighted += run["pass_rate"] * weight
        total_weight += weight
        counted += 1
    if not total_weight:
        return 0.0, 0
    return round(weighted / total_weight, 3), counted


def main(argv):
    parser = argparse.ArgumentParser(description="Aggregate one benchmark iteration.")
    parser.add_argument("iteration_dir")
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--case-file", default=None, help="case file, used for weight, kind, and holdout")
    parser.add_argument("--out", default=None, help="output directory; defaults to the iteration directory")
    parser.add_argument("--executor-model", default=None, help="model that ran the cases; recorded in metadata")
    parser.add_argument("--grader-model", default=None, help="model that graded the runs; recorded in metadata")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    iteration = Path(args.iteration_dir).resolve()
    if not iteration.is_dir():
        print("ERROR: iteration directory not found: " + str(iteration))
        return 1
    out_dir = Path(args.out).resolve() if args.out else iteration
    out_dir.mkdir(parents=True, exist_ok=True)

    schema = load_json(RESULTS_SCHEMA)
    errors = []

    case_meta = {}
    case_file_label = "not supplied"
    if args.case_file:
        case_path = Path(args.case_file).resolve()
        if case_path.exists():
            case_file_label = (
                str(case_path) + " sha256:" + hashlib.sha256(case_path.read_bytes()).hexdigest()[:12]
            )
            data = load_json(case_path)
            for case in data.get("evals", []):
                key = str(case.get("id") or case.get("prompt", ""))[:120]
                case_meta[key] = case
        else:
            print("WARN: case file not found: " + str(case_path))

    cases = []
    configurations = set()
    for eval_dir in sorted(p for p in iteration.iterdir() if p.is_dir() and p.name.startswith("eval-")):
        eval_id = eval_dir.name[len("eval-"):]
        runs = {}
        for config_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir()):
            attempts = collect_runs(config_dir, schema, errors)
            if not attempts:
                continue
            rates = [item["pass_rate"] for item in attempts]
            merged = {
                "pass_rate": round(sum(rates) / len(rates), 3),
                "passed": round(sum(item["passed"] for item in attempts) / len(attempts), 2),
                "failed": round(sum(item["failed"] for item in attempts) / len(attempts), 2),
                "total": attempts[0]["total"],
                "runs": len(attempts),
                "spread": round(max(rates) - min(rates), 3),
            }
            for key in ("tokens", "duration_ms"):
                known = [item[key] for item in attempts if isinstance(item.get(key), (int, float))]
                if known:
                    merged[key] = round(sum(known) / len(known))
            merged["assertions"] = merge_assertions(attempts)
            runs[config_dir.name] = merged
            configurations.add(config_dir.name)
        if not runs:
            errors.append(eval_dir.name + ": no valid grading.json")
            continue

        meta = case_meta.get(eval_id, {})
        baseline = next((name for name in BASELINE_ORDER if name in runs), None)
        with_skill = runs.get(WITH_SKILL)
        entry = {
            "eval_id": eval_id,
            "kind": meta.get("kind", "task"),
            "holdout": bool(meta.get("holdout", False)),
            "weight": float(meta.get("weight", 1)),
            "configurations": {
                name: {key: value for key, value in run.items() if key != "assertions"}
                for name, run in runs.items()
            },
        }
        if with_skill and baseline:
            entry["delta"] = round(with_skill["pass_rate"] - runs[baseline]["pass_rate"], 3)
            entry["baseline"] = baseline
            base_failed = {
                item["text"] for item in runs[baseline].get("assertions", []) if item["passed"] is not True
            }
            with_passed = {
                item["text"] for item in with_skill.get("assertions", []) if item["passed"] is True
            }
            entry["discriminating_assertions"] = sorted(base_failed & with_passed)
            entry["discriminating"] = len(entry["discriminating_assertions"]) > 0
            shared = {item["text"] for item in with_skill.get("assertions", [])} & {
                item["text"] for item in runs[baseline].get("assertions", [])
            }
            passing = {
                item["text"] for item in with_skill.get("assertions", []) if item["passed"] is True
            } & {
                item["text"] for item in runs[baseline].get("assertions", []) if item["passed"] is True
            }
            entry["weak_assertions"] = sorted(shared & passing)
        cases.append(entry)

    baseline_name = next(
        (name for name in BASELINE_ORDER if any(name in case["configurations"] for case in cases)),
        None,
    )
    comparable = [
        case for case in cases
        if baseline_name and WITH_SKILL in case["configurations"] and baseline_name in case["configurations"]
    ]
    excluded = [case["eval_id"] for case in cases if case not in comparable]
    with_rate, with_count = weighted_pass_rate(comparable, WITH_SKILL)
    baseline_rate, baseline_count = (
        weighted_pass_rate(comparable, baseline_name) if baseline_name else (0.0, 0)
    )

    weak = [
        {"eval_id": case["eval_id"], "text": text}
        for case in cases for text in case.get("weak_assertions", [])
    ]
    non_discriminating = [
        case["eval_id"] for case in cases
        if case.get("baseline") and case["configurations"][case["baseline"]]["pass_rate"] >= 1.0
    ]

    def totals(name, key):
        values = [case["configurations"].get(name, {}).get(key) for case in comparable]
        known = [value for value in values if isinstance(value, (int, float))]
        return sum(known) if known else None

    with_tokens = totals(WITH_SKILL, "tokens")
    with_duration = totals(WITH_SKILL, "duration_ms")
    base_tokens = totals(baseline_name, "tokens") if baseline_name else None
    base_duration = totals(baseline_name, "duration_ms") if baseline_name else None

    def drop_missing(entry):
        """Keep unreported cost out of the report instead of reporting a fabricated zero."""
        return {key: value for key, value in entry.items() if value is not None}

    benchmark = {
        "metadata": {
            "skill_name": args.skill_name,
            "iteration": iteration.name,
            "configurations": sorted(configurations),
            "cases": len(cases),
            "case_file": case_file_label,
            "executor_model": args.executor_model or "not recorded",
            "grader_model": args.grader_model or "not recorded",
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        },
        "cases": cases,
        "summary": {
            "with_skill": drop_missing({
                "configuration": WITH_SKILL,
                "cases": with_count,
                "pass_rate": with_rate,
                "tokens": with_tokens,
                "duration_ms": with_duration,
            }),
            "baseline": drop_missing({
                "configuration": baseline_name or "none",
                "cases": baseline_count,
                "pass_rate": baseline_rate,
                "tokens": base_tokens,
                "duration_ms": base_duration,
            }),
            "delta": round(with_rate - baseline_rate, 3),
            "non_discriminating_cases": non_discriminating,
            "weak_assertions": weak,
            "missing_configurations": sorted(
                ({"with_skill"} - configurations)
                | ({baseline_name} - configurations if baseline_name else set())
            ),
            "excluded_cases": excluded,
        },
    }

    (out_dir / "benchmark.json").write_text(
        json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    def show(value):
        return "not reported" if value is None else str(value)

    lines = [
        "# Benchmark: " + args.skill_name + " (" + iteration.name + ")",
        "",
        "Evidence strength: " + str(len(cases)) + " case(s), one run per configuration unless repeated. "
        + "Read this table against the conclusion rules in eval-audit.md; a delta from one or two cases "
        + "is an observation, not a gain.",
        "",
        "Case file at aggregation time: " + case_file_label,
        "",
        "Executed by: " + (args.executor_model or "not recorded") + " | graded by: " + (args.grader_model or "not recorded"),
        "",
        "| Configuration | Cases | Pass rate | Tokens | Duration (ms) |",
        "| --- | --- | --- | --- | --- |",
        "| " + WITH_SKILL + " | " + str(with_count) + " | " + str(with_rate) + " | "
        + show(with_tokens) + " | " + show(with_duration) + " |",
        "| " + (baseline_name or "baseline missing") + " | " + str(baseline_count) + " | "
        + str(baseline_rate) + " | " + show(base_tokens) + " | " + show(base_duration) + " |",
        "",
        "Delta: " + str(benchmark["summary"]["delta"]),
        "",
        "| Case | Kind | " + WITH_SKILL + " | " + (baseline_name or "baseline") + " | Delta | Runs | Spread |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for case in cases:
        with_run = case["configurations"].get(WITH_SKILL, {})
        base_run = case["configurations"].get(case.get("baseline", ""), {}) if case.get("baseline") else {}
        lines.append(
            "| " + case["eval_id"] + " | " + case["kind"] + " | " + str(with_run.get("pass_rate", "missing"))
            + " | " + str(base_run.get("pass_rate", "missing")) + " | " + str(case.get("delta", "n/a"))
            + " | " + str(with_run.get("runs", 1)) + " | " + str(with_run.get("spread", 0)) + " |"
        )
    if non_discriminating:
        lines += ["", "Cases that pass without the skill: " + ", ".join(non_discriminating)]
    for case in cases:
        passing = case.get("discriminating_assertions") or []
        lines += ["", case["eval_id"] + " — assertions that separate the configurations: "
                  + (str(len(passing)) if passing else "none")]
        lines += ["  - " + text for text in passing]
    if weak:
        lines += ["", "Assertions that pass in every configuration:"]
        lines += ["- " + item["eval_id"] + ": " + item["text"] for item in weak]
    if excluded:
        lines += ["", "Cases excluded from the comparison (missing a configuration or invalid grading): "
                  + ", ".join(excluded)]
    if benchmark["summary"]["missing_configurations"]:
        lines += ["", "Missing configurations: " + ", ".join(benchmark["summary"]["missing_configurations"])]

    (out_dir / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for line in errors:
        print("ERROR: " + line)
    if not args.quiet:
        print("wrote " + str(out_dir / "benchmark.json") + " and benchmark.md")
        print("with_skill " + str(with_rate) + " vs " + str(baseline_name) + " " + str(baseline_rate)
              + " (delta " + str(benchmark["summary"]["delta"]) + ")")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
