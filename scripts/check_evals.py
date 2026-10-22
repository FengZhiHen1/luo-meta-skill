#!/usr/bin/env python3
"""Check an eval case file against schemas/evals.schema.json and the skill's fixtures.

Standard library only. Exit code 1 means at least one error.

Usage:
    python check_evals.py [CASE_FILE] [--skill-root DIR] [--schema FILE] [--quiet]

CASE_FILE defaults to <skill-root>/evals/evals.json. JSONL case files are accepted.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_SCHEMA = SCRIPT_DIR.parent / "schemas" / "evals.schema.json"
KNOWN_CASE_FIELDS = {
    "id", "prompt", "expected_output", "files", "assertions", "expectations",
    "kind", "expect_trigger", "holdout", "weight", "source",
}

TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "number": (int, float),
    "integer": int,
    "null": type(None),
}


def resolve_ref(ref, root):
    if not ref.startswith("#/"):
        raise ValueError("only local $ref is supported: " + ref)
    node = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def matches_type(value, expected):
    if expected in ("number", "integer") and isinstance(value, bool):
        return False
    py_type = TYPE_MAP.get(expected)
    return True if py_type is None else isinstance(value, py_type)


def validate(value, schema, root, path, errors):
    """Validate against the JSON Schema subset used by this project's schemas."""
    if "$ref" in schema:
        return validate(value, resolve_ref(schema["$ref"], root), root, path, errors)

    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(matches_type(value, item) for item in types):
            errors.append(path + ": expected " + "/".join(types) + ", found " + type(value).__name__)
            return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(path + ": value " + json.dumps(value) + " is not one of " + json.dumps(schema["enum"]))

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(path + ": shorter than " + str(schema["minLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(path + ": does not match " + schema["pattern"])

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(path + ": below minimum " + str(schema["minimum"]))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(path + ": fewer than " + str(schema["minItems"]) + " item(s)")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                validate(item, schema["items"], root, path + "[" + str(index) + "]", errors)

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(path + ": missing required field " + key)
        properties = schema.get("properties", {})
        for key, sub_schema in properties.items():
            if key in value:
                validate(value[key], sub_schema, root, path + "." + key, errors)
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(path + ": unexpected field " + key)


def load_case_file(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        cases = []
        for number, line in enumerate(text.splitlines(), start=1):
            if line.strip():
                try:
                    cases.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(path.name + ":" + str(number) + ": " + str(exc)) from exc
        return {"evals": cases}
    return json.loads(text)


def lint(cases, skill_root, quiet):
    errors = []
    warnings = []
    seen_ids = {}
    seen_prompts = {}
    holdouts = 0
    anchored = 0
    extra_fields = set()
    alias_users = 0

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            continue
        label = str(case.get("id") or "evals[" + str(index) + "]")
        case_id = case.get("id")
        if case_id is not None:
            if case_id in seen_ids:
                errors.append(label + ": duplicate id (also at evals[" + str(seen_ids[case_id]) + "])")
            seen_ids[case_id] = index

        if "expectations" in case:
            alias_users += 1
        if case.get("kind") == "trigger" and not isinstance(case.get("expect_trigger"), bool):
            errors.append(label + ": kind 'trigger' requires a boolean expect_trigger")
        if "expect_trigger" in case and case.get("kind") not in (None, "trigger"):
            warnings.append(label + ": expect_trigger is ignored for kind '" + str(case.get("kind")) + "'")
        if case.get("holdout") is True:
            holdouts += 1
        source = case.get("source")
        if isinstance(source, dict) and source.get("kind") in ("real", "derived"):
            anchored += 1
        elif source is None:
            warnings.append(label + ": no source declared; record where the task requirement comes from")

        prompt = case.get("prompt")
        if isinstance(prompt, str):
            if prompt in seen_prompts:
                warnings.append(label + ": prompt duplicates evals[" + str(seen_prompts[prompt]) + "]")
            seen_prompts[prompt] = index

        for fixture in case.get("files") or []:
            if not (skill_root / fixture).resolve().exists():
                errors.append(label + ": fixture not found: " + str(fixture))

        extra_fields.update(key for key in case if key not in KNOWN_CASE_FIELDS)

    if alias_users and not quiet:
        warnings.append(str(alias_users) + " case(s) use 'expectations'; write 'assertions'")
    if cases and anchored == 0 and not quiet:
        warnings.append("no case declares a real or derived source; this set can gate exploration "
                        "but cannot support a necessity or quality claim")
    elif cases and anchored < len(cases) and not quiet:
        warnings.append(str(len(cases) - anchored) + " case(s) are synthetic; conclusions must exclude them")
    if cases and holdouts == 0 and not quiet:
        warnings.append("no case is marked holdout=true; tuning on the whole set risks overfitting")
    if extra_fields and not quiet:
        warnings.append("extra fields preserved: " + ", ".join(sorted(extra_fields)))
    return errors, warnings


def main(argv):
    parser = argparse.ArgumentParser(description="Check an eval case file.")
    parser.add_argument("case_file", nargs="?", help="case file; defaults to <skill-root>/evals/evals.json")
    parser.add_argument("--skill-root", default=str(DEFAULT_SKILL_ROOT), help="skill directory that holds evals/")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="case-file schema")
    parser.add_argument("--quiet", action="store_true", help="print errors only")
    args = parser.parse_args(argv)

    skill_root = Path(args.skill_root).resolve()
    case_path = Path(args.case_file).resolve() if args.case_file else skill_root / "evals" / "evals.json"

    if not case_path.exists():
        print("ERROR: case file not found: " + str(case_path))
        return 1
    try:
        data = load_case_file(case_path)
    except (ValueError, json.JSONDecodeError) as exc:
        print("ERROR: cannot parse case file: " + str(exc))
        return 1

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    errors = []
    validate(data, schema, schema, "$", errors)

    cases = data.get("evals", []) if isinstance(data, dict) else []
    lint_errors, warnings = lint(cases, skill_root, args.quiet)
    errors.extend(lint_errors)

    if not args.quiet:
        for line in warnings:
            print("WARN: " + line)
    for line in errors:
        print("ERROR: " + line)
    print(str(len(cases)) + " case(s) checked: " + str(len(errors)) + " error(s), "
          + str(len(warnings)) + " warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
