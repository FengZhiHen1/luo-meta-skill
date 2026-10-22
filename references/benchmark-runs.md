# Benchmark Runs

Read when executing a skill's test set, dispatching executors, grading outputs, or reporting measured results.

## Preconditions

- A case file exists. If it does not, design it first: [test-set-design.md](test-set-design.md).
- A fresh executor is available: a subagent, a separate session, or a child process that starts without this conversation or the skill's design history. Check that the mechanism works before planning runs.
- If no fresh executor is available, do not run the benchmark. Deliver the case file, state what remains unmeasured, and let the user choose another way. Do not execute the cases yourself and present the result as a benchmark.

## Layout

Write results outside the skill directory:

```text
<skill>-workspace/
  iteration-1/
    benchmark.json
    benchmark.md
    eval-<id>/
      with_skill/
        outputs/
        run-notes.md
        timing.json
        grading.json
      without_skill/
        outputs/
        timing.json
        grading.json
```

- `without_skill`: the same prompt with no skill. This is the baseline for a new skill.
- `old_skill`: a copy of the skill as it was before the change. This is the baseline for an improved skill. Copy the skill before editing it.
- Use one iteration directory per full pass. Never mix results from two versions in one directory.

## Executor instructions

Start one executor per run, in the same turn when the harness allows parallel work. Give only the skill path, the case prompt, the input files, and the output directory:

```text
Execute this task.
- Skill: <path to the skill directory, or "none">
- Task: <case prompt>
- Input files: <fixture paths, or "none">
- Save produced files to: <run directory>/outputs/
- Save run-notes.md next to outputs/: which files you read, the main decisions, and anything unresolved.
```

Withhold the expected output, the assertions, the case file, the skill's design documents, and this conversation. Give no hint about the method or the desired result.

## Capture

| Artifact | Content |
| --- | --- |
| `outputs/` | every file the case cares about |
| `run-notes.md` | files read, decisions, uncertainties, unresolved items |
| `timing.json` | `{"total_tokens": 0, "duration_ms": 0}` from the completion notice, written when the run finishes; this data is not recoverable later |
| transcript | the harness trace, when the harness records one |

## Repetitions

Run each case once by default. Repeat three times when the verdict is close, a case looks flaky, or the change is high risk, and report the spread rather than the best run.

## Grading

Grade in the cheapest layer that can decide the question.

1. **Script checks.** Run a validator, test, or inspection script for every assertion a machine can decide. Record the command and its result.
2. **Grader agent.** Give a fresh agent the outputs, the run notes, and the assertions. It writes `grading.json`:

```json
{
  "assertions": [
    {"text": "Both axes are labeled", "passed": false, "evidence": "Y axis reads Revenue ($); the X axis has no label"}
  ],
  "summary": {"passed": 0, "failed": 1, "total": 1, "pass_rate": 0.0},
  "assertion_feedback": ["The image check would also pass for an empty chart"]
}
```

   Grading rules for that agent:
   - The burden of proof is on the assertion. No evidence means fail.
   - Surface compliance fails: a correct file name with wrong content is a fail.
   - Cite the artifact or the trace, not an impression.
   - Report assertions that would also pass for a clearly wrong output, and important outcomes no assertion covers.
3. **Blind comparison.** For subjective quality, give a fresh agent two outputs labeled A and B with the case prompt only, and keep the answer key in a separate file that the judge never reads. Use it when both outputs pass the mechanical checks but one is clearly better, or when a change is claimed to improve quality.

Do not grade a run you executed, and do not treat the author's own reading as independent grading. Label self-review as self-review.

## Read the results

| Signal | Meaning | Action |
| --- | --- | --- |
| fails without the skill, passes with it | the case discriminates | keep it |
| passes in every configuration | no evidence of value | test a harder boundary, or drop the case and state that the skill adds nothing there |
| fails in every configuration | the skill does not cover it, or the case is out of scope | fix the skill, or move the case out of scope |
| pass rate rises but cost rises sharply | a trade-off, not a gain | report both numbers |
| assertions pass in every run regardless of output | weak assertion | rewrite or remove it |

Aggregate with `scripts/summarize_runs.py <iteration directory> --skill-name <name>` from the skill root to produce `benchmark.json` and `benchmark.md`. Read [results.schema.json](../schemas/results.schema.json) when writing these files by hand.

## Report

- State the comparison behind every number: with skill against no skill, or this version against the previous one.
- Distinguish three states: structure checked, design reviewed, runtime behavior tested. A trigger change read as text is a design review, not a test.
- Mark missing evidence as missing. Do not turn an expectation into a result.
- Stop when the cases pass in the target configuration, the remaining failures are out of scope, or further edits stop moving the numbers. Say which of these happened.
