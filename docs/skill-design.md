# Luo Meta Skill Design

Status: independent rewrite. Runtime behavior is authoritative in `SKILL.md` and `references/`; this document records design intent, source trade-offs, and maintenance boundaries. It does not duplicate runtime rules.

## Goals

Help an agent create, refactor, and improve reusable Agent Skills, with emphasis on domain expertise, execution structure, and real-task outcomes.

## Non-goals

- No unified CLI, Skill OS, platform compiler, or release governance system.
- No mandatory evaluation platform, evidence ledger, scorecards, or review studio. Benchmarking is an on-demand capability, not a release gate; the skill ships no CI, no report service, and no baseline store.
- Do not package one-off tasks, single-repository conventions, or deterministic rules as skills.
- Do not copy any upstream project's directory structure or maintenance rituals.

## Design principles

- Task triage: fix small issues directly; research and design only for a new capability, material change, or diagnosis.
- Shape selection: choose a starting organizational shape (procedure, knowledge, tool, judgment, creative), allow hybrids, and adapt it to the task. Shapes are patterns, not categories or gates.
- Two-anchor research: real tasks and capability gaps complement systematic domain knowledge.
- Specification and runtime separation: project `docs/` maintains intent, behavior, implementation, and acceptance; runtime contains only what execution needs.
- Description as a routing contract: the harness reads it before the body; state the job and trigger boundary in the language of the requests it must catch, keep the shortest wording that preserves the boundary, and do not summarize the workflow.
- Language follows the audience: local skills use the language of their requests; skills with an international audience use English as the primary language and add other terms only when they change routing.
- Precise technical instructions: settle semantics first, then choose constraint strength by behavior fragility. Borrow ASD-STE100 clarity principles without claiming conformity. Apply them only to technical runtime instructions, not to creative output or source material.
- Knowledge freshness and organization: keep durable guidance in the skill, refresh volatile facts, and organize runtime references by task rather than by source. The main path may rely on references when the entry point routes the agent to them before use.
- Proportionate verification: choose checks by the changed behavior, risk, and uncertainty. Trigger checks apply to trigger changes; artifact, loading, execution, and contract checks apply to their respective changes. Distinguish designed test cases from observed failure evidence.
- Test sets answer two questions: whether the skill is necessary, and whether this version is better. The necessity answer comes from running the same cases with no skill and with the skill; a case the bare agent already passes measures nothing.
- Measurement requires an independent executor. A fresh agent, session, or process starts without the authoring history; without one, the skill delivers the case set and states what remains unmeasured instead of self-running it.
- Harness neutrality: a harness is the agent runtime that discovers, loads, and runs skills. Verify platform mechanisms before relying on them; never assume availability from a file name.
- Structured artifacts get one schema: keep field names, types, and value domains in one machine-readable schema (for example, `schemas/`) only when code, tests, or a validator consume it; derive code and tests from it.
- Reference routing as a decision: every reference needs a read-when, plus a skip-when when over-reading is a risk; the default path should need no reference; a file index is not routing.

## File organization

- `SKILL.md`: task triage, skill-worthiness decision, reference routing, core design principles, verification and delivery, stop and hand-back conditions.
- `references/research-and-synthesis.md`: two-anchor research, source evaluation, knowledge conversion, external skill adaptation.
- `references/skill-architecture.md`: scope and boundaries, `SKILL.md` body shape, specification documents, runtime structure, trigger boundary and case design, harness compatibility.
- `references/instruction-craft.md`: semantics first, constraint strength, technical writing rules, trigger descriptions, revision strategy, precision check.
- `references/reference-routing.md`: routing contract, formats, anti-patterns, routing tests.
- `references/iteration-and-evaluation.md`: failure diagnosis, proportionate evaluation, trigger and output checks, honest reporting.
- `references/test-set-design.md`: two-question framing, case families, prompt and fixture design, assertion discriminating test, trigger and pressure cases, holdout, default case format and foreign-format mapping.
- `references/benchmark-runs.md`: executor preconditions, run layout, isolation rules, capture, repetitions, three grading layers, weak-assertion and necessity reading, reporting.

The seven references are routed by task and are not all loaded at startup.

`scripts/check_evals.py` and `scripts/summarize_runs.py` exist because both tasks are deterministic and repeated: validating a case file against `schemas/evals.schema.json`, and aggregating run results into `benchmark.json` and `benchmark.md`. Both use the Python standard library only, so no dependency changes. Grading stays with an agent and a written rule set; it is judgment, not a script.

`schemas/evals.schema.json` and `schemas/results.schema.json` are the single authoritative definition of the case file and the run result files. The scripts read the schemas instead of restating field rules.

`evals/` holds this skill's own test set and fixtures. It ships with the skill because it is part of the product: it is how a change to this skill can be shown to help or to hurt. Run results stay outside the skill directory.

## Source trade-offs

| Source | Adopted | Not copied |
| --- | --- | --- |
| Sentry skill-writer | Source research, source adaptation, on-demand references, precision checks, no-first-person description rules | Mandatory SPEC, fixed coverage matrix, registration process |
| OpenAI skill-creator | Runtime economy, matching freedom to task fragility, resource responsibilities, description as the only trigger surface | Harness-specific initialization and UI metadata |
| Anthropic skill-creator | Real artifact feedback, trigger checks, with-skill and without-skill runs in fresh executors, evidence-citing grading, blind comparison for subjective quality, assertion critique | Mandatory full evaluation pipeline, dedicated viewer and script suite, required subagents |
| Superpowers writing-skills | Use failure scenarios and pressure tests to expose instruction gaps, workflow summaries in descriptions can displace the body | The absolute requirement to write a failing test before every change |
| Yao Meta Skill | Non-skill decisions, nearby triggers, portability awareness, trigger-first authoring, conditional exclusions, shorter-wins, separate answer key for blind review, missing evidence stays missing, holdout rotation | Skill OS, unified IR, release gates, governance, execution-evidence ledger |
| Skillet | One case per known failure mode, fixtures that reproduce the failure | Spec-first authoring flow |
| Agent Skills specification | Minimum metadata, progressive disclosure, on-demand references, the `evals/evals.json` case shape | Treating recommended practices as mechanisms every harness supports |
| ASD-STE100 | Consistent terms, explicit actions, conditions, low-ambiguity expression | Controlled dictionary, certification claims, uniform sentence length |

This is an independent synthesis of methods. It does not copy protected upstream text.

## Relationship to the legacy implementation

An earlier implementation was a branch of yao-meta-skill with scripts, evaluation, governance, and an evidence system. It is not part of this repository. The public version does not inherit its directory structure or process.

## Maintenance rules

- When behavior, scope, or implementation choices change, update this document and the affected references.
- A wording-only change does not require a new snapshot, version file, or duplicate document.
- When a real task exposes a design problem, fix the runtime guidance first and then update the rationale here.
- Keep iteration records, evaluation output, and one-off research out of the distributed skill.
- Keep the distributed skill self-contained. Do not reference the author's repository layout, local instruction files, or workspaces from runtime content; local conventions may inform the implementation, but the skill must carry the rules it needs.
- Keep this skill's own `description` and runtime guidance in English. It is an international open-source product; do not localize its metadata to the author's local language.

## Validation plan

These are smoke-test cases, not executed results.

| Task | Expected behavior | Observe |
| --- | --- | --- |
| Spelling-only fix in an existing skill | Edit the affected text; do not start a research pass or create new documentation | Diff and execution trace |
| Description that summarizes the workflow | Rewrite it as job plus trigger boundary; the agent still reads the body and follows every step | Description text and execution trace |
| Complex presentation skill with homogeneous layouts | Inspect the current skill and real pages; research layout decisions; produce conditional guidance with trade-offs and examples; keep the working generation pipeline | Guidance quality and resulting pages |
| LaTeX skill with unstable cross-platform compilation | Check compiler and tool versions; write exact commands and failure recovery; preserve freedom in academic writing | Commands, failure handling, compiled output |
| One-off file-rename request | Do not create a skill; perform the task or recommend a tool | Whether extra files were created |
| Request to use an existing presentation skill | The meta-skill does not trigger | Harness routing trace |
| Target harness lacks a Claude-only extension | Do not fake portability; choose an available alternative and state the limitation | Harness capability check |

Text, structure, and reference checks are complete for the runtime files, the schemas, and the own test set (`evals/evals.json` passes `scripts/check_evals.py`). The cases above are a design plan, not executed results. Cross-harness behavior evaluation of this skill is not complete. One case of the own test set has been run end to end once, with and without the skill in independent executors: the measured delta is small and four of six assertions did not discriminate, so the capability claim stays open.
