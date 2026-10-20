# Iteration and Proportionate Evaluation

Read when improving a skill from usage evidence, measuring behavior, checking trigger quality, or comparing revisions.

## Diagnose before changing text

Collect as much as possible: the original request, available inputs, the skill and references actually selected, the execution trace, the final artifact, and user feedback. Separate observation from interpretation. Test cases designed from known requirements or boundaries are useful, but are not evidence of observed failures.

| Observation | Check first |
| --- | --- |
| Skill not triggered, or triggered for an unrelated task | `description`, nearby competing skills, harness trigger mechanism |
| Important reference not read | Routing condition, path correctness, file discovery, harness loading mechanism |
| Model followed instructions but output is still weak | Missing domain knowledge, weak decision criteria, insufficient examples or tools |
| Output violates a format or API contract | Incorrect technical detail, ambiguous instruction, missing deterministic check |
| Unnecessary operations performed | Trigger too broad, mandatory research or evaluation wording, unclear default or stopping condition |
| A previously working task fails after an edit | Lost behavior, conflict between old and new rules, regression in a shared dependency |

Do not assume that another prompt rule will fix a missing tool capability or a wrong specification.

## Choose evidence proportionate to risk

- Small fix: check the affected instructions, paths, and structure. Behavior evaluation is usually unnecessary.
- Behavior change: select representative tasks and important boundaries for the changed behavior. Check domain knowledge through resulting artifacts, reference routing through loading traces, and tool or format changes through execution and contract checks. For trigger changes, also check missed triggers and nearby non-trigger requests. Inspect actual artifacts and traces, not model self-reports.
- Important or uncertain result: compare before and after on the same tasks, or compare with and without the skill.
- High variance or high risk: add cases, repetitions, and independent review. Expand evaluation only when the conclusion justifies the cost.
- Risk of overfitting: keep a few holdout examples out of tuning. Do not treat fixed evaluation prompts as the product specification.

Match evaluation to the domain. Compilation and exact schemas can be checked automatically. Technical writing needs semantic review. Presentation design needs real visual artifacts; a text-only reviewer must not pretend to inspect pixels. When using independent review, state clear criteria. A model score is evidence, not proof.

## Trigger evaluation

Collect real positive and negative cases:

- Different natural phrasings of the same task;
- Typical requests that should trigger;
- Nearby requests that should not trigger (executing an existing skill, one-off tasks, ordinary documentation edits);
- Neighboring skills with overlapping terminology;
- The languages and shorthand that users actually use.

Test actual trigger behavior in the target harness. Do not infer all harnesses from one harness's result, and do not overfit to synthetic phrases. After changing triggers, check both missed triggers and false triggers.

Also check description/body consistency: every capability named in the description must exist in the skill, and every capability removed from the skill must leave the description. A description that promises a capability the skill does not deliver causes the agent to load the wrong skill or improvise.

## Output and behavior evaluation

Check:

- Whether necessary references were read;
- Whether unnecessary steps were performed;
- Whether the artifact reaches domain quality, not only correct format;
- Whether exact contracts and failure boundaries were followed;
- Whether the agent stopped when it should;
- Whether the user needs substantial rework.

Review the artifact itself. Self-assessment, summaries, and model self-reports do not replace real output.

## Fix the smallest cause

Locate the layer of the problem:

- Wrong goal or scope;
- Weak source quality;
- Missing or conflicting runtime guidance;
- Reference not loaded;
- Tool or environment mismatch;
- Unreasonable acceptance criteria.

Replace, narrow, or delete the corresponding content. Do not use a new rule to hide a problem in an old rule. Update `docs/` only when intent, behavior, or implementation choices change. A wording change does not need a new version or snapshot.

## Test reference routing

Use three representative tasks: the default path, one branch that needs a reference, and one neighbor that should read none. Ask a reader who did not write the skill, or walk the three tasks as a new reader, which file they would read and which they would skip. If they cannot choose without opening the files, the route is unclear or missing. Also check that every reference is reachable exactly once and that no file is orphaned.

## Report honestly

State exactly what was done:

- Manual review;
- Metadata and path checks;
- Safe script or test execution;
- Real task execution;
- Before/after comparison or a no-skill control;
- User acceptance.

Also state untested harnesses, quality dimensions, and known gaps. Without a real comparison, do not claim a measured skill gain.
