# Research and Knowledge Synthesis

Read when the skill needs new domain knowledge, absorption of an external skill, or a material change to professional content.

## Goal

Convert sources into runtime capability. The output of research is not a link list or a source-coverage matrix. It is better judgment, operations, and checks that the agent will use in real tasks.

## Two anchors

### Task anchor

Collect a small set of representative tasks: real requests, expected artifacts, current practice, and known errors. Focus on:

- Which decisions are non-obvious and lack facts or decision cues?
- Which operations are fragile in sequence, parameters, or environment?
- Which tools, formats, or interfaces must be exact?
- Which quality criteria appear only in real artifacts?

When execution evidence is absent, mark a suspected gap as a hypothesis and state which design choice it affects.

### Domain anchor

Map the knowledge that a competent practitioner uses:

- Main methods and their applicable conditions;
- Key distinctions and common misunderstandings;
- Accepted tools, versions, and alternatives;
- Professional disagreements and the grounds for each;
- Difficult boundaries, failure modes, and recovery methods;
- Representative success and failure examples.

The task anchor sets research priorities. The domain anchor finds blind spots that current failures have not exposed. The two do not require separate reports.

## Select and evaluate sources

| Question | Preferred sources | Caution |
| --- | --- | --- |
| Exact API, format, protocol, or support scope | Official specifications, versioned documentation, implementation code and tests | Check the target harness and version; documentation may lag implementation |
| What works in production | Maintained implementations, runbooks, issue resolutions, migration records, reproducible examples | A single workaround is not a general rule |
| Professional quality and aesthetics | Domain experts, influential references, analyzed work samples, paired success and failure cases | An official product page is not necessarily the best quality authority |
| Actual skill behavior | Execution traces, real artifacts, user corrections, review records, regression cases | Distinguish observation, inference, and preference |
| Community experience | Discussions, author explanations, community tests | Check dates, sample sizes, and reproducibility |

For factual claims that affect conclusions, prefer original, current evidence that matches the target environment. When reading strong skills, examine mechanisms. Do not treat any project as the standard architecture: task triage, on-demand loading, failure-driven improvement, expertise conversion, and trigger design can all be evaluated separately.

## Stopping conditions

Stop when further search is unlikely to change a material design choice. Continue when:

- A critical interface or boundary remains unclear;
- The domain has a material disagreement and the current design uses only one side;
- A known failure cannot be explained by current knowledge;
- New material could overturn the current default path.

Do not continue merely to increase the source count, repeat existing conclusions, or collect background unrelated to the task.

## Convert sources into runtime capability

For each important finding, ask: what will the agent decide, do, remember, or verify differently because of this?

| Finding type | Runtime form | Must preserve |
| --- | --- | --- |
| Decision cue | Decision criteria, priorities, counterexamples | Applicable conditions, trade-offs |
| Technical operation | Ordered steps, exact parameters, failure recovery | Sequence, values, units, error boundaries |
| Exact fact | Concise reference, schema, version note, or runtime lookup | Source version, applicable scope, freshness |
| Implicit distinction | Paired success and failure examples | The reason for the difference, not only the conclusion |
| Repeated or fragile operation | Tested script or tool | Input/output contract, failure behavior |

Do not write general knowledge that the model already has. Do not turn conditional professional advice into absolute rules unless a hard invariant exists. Do not compress open judgment into a single if/else.

## Keep runtime knowledge usable

### Separate durable knowledge from volatile facts

Design principles, decision methods, and stable procedures age slowly. API versions, model limits, quotas, prices, and service behavior change.

Keep durable guidance in the skill. For volatile facts, state the version or date, require a check against current authoritative sources before use, or provide a short retrieval step. Do not present a volatile fact as permanent truth.

### Organize by task, not by source

Sources are organized by origin: websites, courses, repositories, papers. Runtime references should answer the questions the agent must decide, the actions it must perform, and the failures it must diagnose.

Do not mirror the source tree. Group knowledge by use. When the set grows, use routing or a shallow index and keep the entry path short. Avoid multi-hop lookups that hide essential guidance.

## Adapt an external skill or workflow

1. State the source's purpose and the problem it solves.
2. Identify the capability that is genuinely useful for this project, not the whole file structure to copy.
3. Check the target harness's tools, permissions, loading mechanism, and version limits.
4. Determine which semantics must survive: trigger conditions, safety boundaries, exact contracts, professional trade-offs.
5. Rewrite in independent language. Check licenses and attribution before copying protected material.
6. Record meaningful sources, their version or commit, reasons for adoption, and reasons for rejection in `docs/`. Do not put source arguments into runtime references.

Do not mechanically copy section order, commands, test counts, or maintenance rituals. A source is evidence and a method library, not an architecture standard.

## Common failures

- Collect many links but change no agent behavior.
- Use source count, file count, or section completeness as a substitute for capability judgment.
- Turn a single case, a personal preference, or one product's practice into a general rule.
- Patch only the failures that have already been reported and ignore more important domain risks.
- Force a professional disagreement into one answer and lose the applicable conditions.
- Put maintenance background, research history, or author notes into runtime context.
- Mirror the source's structure in runtime references.
- Bundle volatile facts as permanent truth.

## Division of labor with documentation

- `docs/`: research conclusions, sources, trade-offs, acceptance methods, and open questions. For maintainers.
- `references/`: professional knowledge, methods, and exact material that the agent consults during a task. Loaded on demand.
- `SKILL.md`: main path, default behavior, key boundaries, and reference routing.
