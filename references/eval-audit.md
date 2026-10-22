# Eval Audit

Read when judging whether a test set is sound: before trusting a benchmark result, before running cases someone else wrote, or when reviewing a set you just produced.

A test set is an instrument. Audit the instrument before you read the measurement.

## Four properties

| Property | Question | Failure signal |
| --- | --- | --- |
| Anchor | does each case come from a real task requirement | the prompt exists because it is convenient to grade |
| Discrimination | can each case fail without the skill | the bare agent passes it |
| Baseline validity | was the baseline actually without the skill | nothing shows the skill was unavailable |
| Conclusion fit | does the set support the claim being made | one case, one run, reported as a gain |

## Audit one case

- Read the prompt as a user would send it. Does it carry the real inputs, the real ambiguity, and the real constraints?
- Read the provenance note. What does the task requirement come from, and what was adapted? An adaptation that adds difficulty proves nothing about real work; one that removes the hard part hides failures.
- Name a plausible wrong output that would pass every assertion. If you can name one, the case is too weak.
- Check the baseline design: same prompt, same inputs, no skill discoverable. A baseline that loses the input files, the messy data, or the deadline is not a baseline.
- Check the holdout: if it was edited after a failure, it is no longer a holdout.

## Verdict per case

| Verdict | Use when |
| --- | --- |
| keep | anchored, discriminating, and the baseline is safe |
| rewrite | the failure mode is real but this prompt or assertion cannot expose it |
| drop | nothing anchors it, or it cannot discriminate |

## Audit the set

- **Coverage.** Do the cases cover the request shapes that actually occur, including the expensive tail? Two cases of the same shape measure that shape twice.
- **Family balance.** One family dominating says nothing about the others. A set of only `task` cases cannot show trigger or contract behavior.
- **Independent cases.** How many cases can fail on their own? A set where one case carries the verdict is a single observation, not a benchmark.
- **Author bias.** Which cases did the author invent, and which requirement do they stand for? A set written from the author's idea of the task measures the author's imagination.
- **Instrument drift.** Were assertions, prompts, or fixtures changed after a failure was seen? Say so, and read the result against the earlier version instead of comparing across the change.

## Conclusion strength

State what the evidence supports before stating the number:

| Evidence | The claim it supports |
| --- | --- |
| several anchored cases, each discriminating or explained, verdict read from holdout | this version does better on these task shapes |
| one or two cases | an observation about those cases only |
| every case passes without the skill | the skill adds nothing on these cases |
| only unanchored cases | exploration; no necessity or quality claim |
| delta inside the noise band | no observed difference |

Never convert an observation into a measured gain, and never let a rerun of the same case stand in for a second case.

## When a set is handed to you

1. Read the case file and the provenance notes, not the result summary.
2. Produce a verdict per case and one verdict for the set.
3. Name the smallest change that would make the intended claim valid: a harder assertion, one more anchored case, a real baseline, or a holdout.
4. If the set cannot support its claim at all, say that first, before discussing the numbers.

An audit is cheap compared with a run. Do it before spending executors, and again before reporting, because the failures you saw will tempt you to loosen the instrument.
