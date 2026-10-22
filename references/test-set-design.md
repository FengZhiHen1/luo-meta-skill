# Test-Set Design

Read when designing or revising a skill's test cases, or when deciding what evidence would show that a skill is necessary and good.

## Two questions, one case set

| Question | Comparison | Reading |
| --- | --- | --- |
| Is the skill necessary? | the same cases with no skill and with the skill | a case the bare agent already passes produces no evidence of value |
| Is this version better? | the same cases with the previous version and the current version | gain, cost, and failure type per case |

A case earns its place in one of two ways: it fails without the skill, or it reproduces a failure someone actually observed. Cases that pass in every configuration measure nothing; keep one as a smoke check if it is cheap, and say that it measures nothing.

## Case families

| Family (`kind`) | Purpose | Include when |
| --- | --- | --- |
| `task` | realistic end request; the skill must produce the artifact | always |
| `trigger` | requests that must trigger and near misses that must not | the skill competes with neighbors, or triggering is the reported problem |
| `contract` | exact format, interface, or failure boundary | the skill carries a fragile contract |
| `pressure` | a request that invites skipping the skill's discipline under combined pressure | the skill enforces a process that costs effort |
| `routing` | whether the agent reads the needed reference and skips unneeded ones | the skill has several references |
| `diagnosis` | a reported failure must be located before anything is edited | the skill is used to repair other skills or artifacts |

Start with two or three `task` cases. Expand from observed failures, not from an imagined coverage matrix.

## Anchor every case in a real task

A case may be a request captured almost verbatim, or a prompt written for the case. Both are valid. What is not valid is a prompt that exists only because it is convenient to grade.

A case matches the real task when it keeps:

- the real inputs and their defects;
- the ambiguity the requester actually leaves;
- the real constraints and deadline;
- the artifact the requester actually needs;
- the requester's actual level of knowledge.

Adaptation rules:

- Keep the original wording when you have it. Replace names, paths, and identifiers to remove private data without making the task cleaner.
- Never add a hint, the method, or the expected output.
- Never add difficulty the real task does not have, and never remove the part that makes it hard.
- Use the file names, tool names, domain terms, and shorthand or mixed language the audience really uses.
- One task per prompt. Bundle requests only when real users bundle them.
- Make the request substantial enough that a capable agent benefits from instructions. A one-step request tests nothing.

Sources for real task requirements: past requests and session history, issue and pull-request threads, support tickets, chat, failure reviews, and the user's own prompts. Ask for two or three when nothing is on hand.

Record the provenance in the case:

```json
"source": {"kind": "derived", "note": "adapted from a failed weekly-report request; kept the missing-field data, removed the company names"}
```

`kind` is `real` for a captured request, `derived` for a prompt written from a real requirement, and `synthetic` for no real anchor. A set of only `synthetic` cases can gate exploration; it cannot support a claim about necessity or quality. Audit the set with [eval-audit.md](eval-audit.md) before you trust its numbers.

## Provide inputs

- Put input files under `evals/files/` and reference them from the case.
- Build each input so the intended failure mode is reachable: a half-built artifact, a weak draft, a malformed record. A clean input hides the problem the case exists to catch.
- Keep long material in files, not inside the prompt.

## Describe expected output

State success as a reader would judge it: the artifact, its required properties, and the boundary that must hold. Do not write a checklist of phrases to include.

## Write assertions

Add assertions after the first run, when you can see what a real output looks like. Each assertion must be checkable from the produced artifact or trace.

| Assertion type | Use for | Written as |
| --- | --- | --- |
| script-checkable | file existence, structure, counts, validator result, forbidden strings | a statement a script or grader can decide mechanically |
| evidence-based judgment | domain quality, routing, adherence to a boundary | a statement plus the artifact that proves it |
| no assertion | taste, style, audience fit | human review or blind comparison |

**Assertion quality test.** For each assertion, name a plausible wrong output that would still pass. If you can name one, replace the assertion. An assertion that rewards mentioning a word, creating a file, or restating the prompt is worse than no assertion: it creates false confidence.

Negative properties are the strongest assertions: a forbidden file, an absent section, a boundary that must not be crossed.

## Trigger cases

- Write positive cases as different phrasings of the same intent, including requests that never name the artifact.
- Write negative cases as near misses: requests that share vocabulary or domain but need a different response. Obviously unrelated requests test nothing.
- Use the languages and shorthand of the real audience.
- Check both directions after a change: missed triggers and false triggers.

## Pressure cases

Use only for skills that enforce a process that costs effort, and only when compliance can be rationalized away.

- Combine at least three pressures: deadline or emergency, sunk cost, authority, fatigue, social cost.
- Give concrete competing options and require a choice and an action.
- Make the scenario concrete: real paths, real consequences, no hypothetical framing.
- Record the rationalizations executors produce without the skill, and use them to test whether the skill closes that specific hole.

## Hold out cases

Keep one or two cases out of tuning, and read the verdict from them. A test set edited after every failure stops describing the task and starts describing what you already built.

Fixed cases are not the product specification. Generalize from a failure to its cause; do not add an instruction for the failing prompt.

## Format

The default case file is `evals/evals.json`, using the Agent Skills eval shape:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "top-months-chart",
      "prompt": "I have a CSV of monthly sales in data/sales.csv. Find the top 3 months by revenue and chart them.",
      "expected_output": "A bar chart image of the top 3 months, with labeled axes.",
      "files": ["evals/files/sales.csv"],
      "assertions": ["The output includes an image file", "Both axes are labeled"],
      "kind": "task",
      "holdout": false,
      "weight": 1
    }
  ]
}
```

`prompt` is the only required case field. Optional case fields: `id`, `expected_output`, `files`, `assertions`, `kind`, `expect_trigger`, `holdout`, `weight`, `source`.

- `kind` is one of `task`, `trigger`, `contract`, `pressure`, `routing`, `diagnosis`. The default is `task`.
- `expect_trigger` applies to `kind`: `trigger` only.
- `holdout` marks a case excluded from tuning.
- `weight` defaults to `1`.
- `source.kind` is `real`, `derived`, or `synthetic`; `source.note` says what was adapted.

Read other formats when the project already has them. Normalize into this model and report what you mapped, what you dropped, and what you inferred. Conflict resolution prefers the default file.

| Existing format | Mapping |
| --- | --- |
| trigger files with `should_trigger` and `should_not_trigger` arrays of `text` | one `trigger` case per entry, `expect_trigger` set from the array |
| JSONL case files, one object per line | one case per line, same field names |
| scenario files with `prompt`, `judge` checks with weights, `setup` copies, `artifacts` globs | `judge` check becomes an assertion, its weight becomes `weight`; `setup` becomes fixture preparation; `artifacts` becomes an output check |
| keyword-weight configuration used to tune a description | not a case set; use it as description input and say so |

Preserve unknown fields. Accept `expectations` as an alias of `assertions`; write `assertions`.

Validate the case file with `scripts/check_evals.py` from the skill root before running it.
