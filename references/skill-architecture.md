# Skill Scope, Specification, and Structure

Read when creating a new skill, materially changing its runtime structure, or deciding how specifications, references, scripts, and harness mechanisms should be divided.

## Define the task family and boundaries

Use concrete requests to determine:

- Target users and the task family;
- What counts as success;
- Which requests should trigger the skill;
- Which nearby requests should not trigger it;
- Boundaries with existing skills.

When changing an existing skill, start from its current behavior and project constraints. Do not rewrite the structure first.

## Decide whether to create a skill

| Need | Better fit |
| --- | --- |
| A request that happens once and will not recur | Complete it directly |
| A convention for one repository only | Project instructions or project documentation |
| A rule that must be enforced exactly | Validator, compiler, test, or policy enforcement |
| Access to an external system or API | Existing connector, CLI, or MCP tool; add a skill when professional usage guidance helps |
| Reusable domain judgment or a professional process | Agent Skill, with scripts and assets when needed |

A skill can contain both methods and tools, but it must center on one coherent task. Avoid one-sentence micro-skills and unbounded everything-skills.

## Specifications and design documents

Maintain the current specification and design in the target skill project's `docs/`, following existing project conventions. One document is enough for a small skill; a complex skill may separate behavior, architecture, interfaces, and evaluation. The documentation should let an implementer who did not join the conversation understand the design.

Include as needed:

- Intent and scope: target users, task family, triggers and exclusions, promised value, and non-goals.
- Justification: why a skill is needed rather than a one-off response, project instruction, existing tool, or documentation.
- Expected behavior: important outputs, task branches, dependencies, failure boundaries, and exact contracts.
- Implementation design: knowledge strategy, runtime entry point, reference routing, deterministic tools, harness dependencies, major trade-offs, and rationale.
- Evidence and acceptance: representative tasks, real outcomes or risks, suitable validation methods, and open questions.

Do not turn these items into a mandatory template, and do not fill every field for its own sake. Keep only the information needed to implement and maintain the skill. A wording-only change that does not change intent or behavior does not require a new specification version.

## Choose a starting shape

These are organizational starting points, not categories. A skill may combine shapes. Use the shape to choose default components and the first validation case. Do not add metadata, mode names, or gates for a shape; add only what the task needs.

| Shape | Default structure | Main risk |
| --- | --- | --- |
| Procedure or workflow | Ordered steps; scripts for deterministic or fragile steps; stop and exception conditions; references only for branch-specific knowledge | Skipped steps, unclear recovery |
| Knowledge | Task-routed references; freshness handling for volatile facts; worked examples; minimal procedural text | Source dump, stale facts |
| Tool or interface | Exact contracts; scripts or commands; error boundaries; harness checks; references for exact API details | Silent failure, assumed portability |
| Judgment or review | Criteria; contrasting examples; trade-offs; output format | Rigid if/else, missing discriminating cues |
| Creative production | Quality goals; audience; assets and examples; room for alternatives | Over-proceduralization |

Routing is a mechanism available to any shape. A standalone routing skill also needs a default path, a fallback, and tests for neighboring requests.

## SKILL.md shape

The Agent Skills specification requires frontmatter and leaves the body format open. Define the body by the questions it must answer, not by a fixed set of headings.

| Question | Required content | Avoid |
| --- | --- | --- |
| What does it do, and what is the default outcome? | One or two sentences: task family, default output, scope. | A duplicate of the description, a workflow summary, or background. |
| What is the default path? | Ordered steps or a decision flow; the default when several paths exist; conditions next to the action they govern. | Principles without actions, every branch expanded, design rationale. |
| What should I read, and when? | One routing block with a default, a read-when, and a skip-when when over-reading is a risk. See [reference-routing.md](reference-routing.md). | A file index, "read as needed", nested knowledge references. |
| When do I stop, fail, or hand back? | Execution boundaries; failure, stop, and hand-back conditions; permission and safety boundaries; recovery. | Trigger exclusions, "handle errors appropriately", no stopping condition. |
| How do I know the task is complete? | A completion check, the output contract when fixed, and the evidence required. | "Verify as appropriate", a scorecard instead of a completion condition. |

The questions are required; the headings are not. Use the smallest structure that makes each answer findable.

A default skeleton:

```markdown
# <Title>
<One or two sentences: job, default outcome, scope.>

## Main path
<Default steps or decision flow. State the default when several paths exist.>

## Reference routing
<Default: no reference. Read X when ...; skip when ...>

## Boundaries and failure handling
<Execution scope. Stop, fail, ask, or hand back when ...; recover by ...>

## Completion check
<How to know the task is done; output contract; evidence.>
```

Add only the optional blocks that change a decision, action, or verification:

- a decision table or selection guide when the main path branches;
- gotchas or common mistakes for known, repeated failures;
- a quick reference for scanning, not as a substitute for the main path;
- input/output examples or contrasting examples;
- an output template; put large templates in `assets/`;
- an operating contract for complex or tool skills: primary output, tools, failure tolerance;
- assets or scripts usage.

Match the blocks to the shape in [Choose a starting shape](#choose-a-starting-shape). A procedure needs checkpoints and stop conditions; a knowledge skill needs selection criteria and freshness; a tool skill needs exact contracts and error boundaries; a judgment skill needs criteria, cues, and trade-offs; a creative skill needs goals, audience, constraints, and room for alternatives.

Do not put status, history, version, changelog, ownership, design rationale, source arguments, or iteration records in `SKILL.md`; keep them in `docs/` or repository metadata. Do not add a "When to use" section; the description owns the trigger. Do not add README, CHANGELOG, or QUICK_REFERENCE files as runtime files inside a skill; repository metadata is separate. Do not write unverified harness mechanisms, absolute paths, other repositories, or local machine locations.

Keep the body under the specification's guideline of about 500 lines and 5,000 tokens. If it grows, remove duplicated reference material, rationale, and edge cases the agent can handle; split a genuine branch into a reference rather than cutting the main path. The body carries the main path; references carry task-time detail; `docs/` carries design intent.

## Runtime structure

Start with one coherent `SKILL.md` and add components only when the work needs them:

- `references/`: substantial domain knowledge needed only in some task variants. State when to read each file and when not to.
- `scripts/`: deterministic transformations, repeated calculations, or fragile tools. A script should have clear inputs and outputs and be verified on representative safe cases.
- `assets/`: templates, design examples, input/output materials, and other resources needed to produce results.
- `schemas/`: optional machine-readable contracts for structured artifacts (JSON Schema, SQL DDL, or equivalent), only when code, tests, or a validator consume them. Keep one authoritative definition and derive code and tests from it; do not duplicate field rules in prose.
- Routing: establish it only when inputs genuinely select different knowledge or tools. Provide a default path and make ambiguous cases recoverable.
- Subagents, hooks, execution isolation, special frontmatter: use only when the target harness actually supports them and the benefit can be measured. Do not assume that one harness shares another harness's mechanisms.

Reference routing is a separate design problem. Use [reference-routing.md](reference-routing.md) to decide what to read, when, and when to skip it; a list of files is not routing.

Keep knowledge references flat: `references/<name>.md`, so every file is one level from `SKILL.md`. Assets and scripts may use subdirectories. Do not build chains that hide essential guidance. A correct relative path does not prove that the harness can discover the reference. Check loading behavior in the real harness.

## Trigger design

Define the trigger boundary before writing the description. Decide which task family the skill owns, which requests must stay outside it, and which neighboring skills could be confused with it.

When designing triggers, check:

- Whether different phrasings of the same task are recognized;
- Whether requests to execute an existing skill are wrongly triggered;
- Whether terminology overlap with a neighboring skill causes confusion;
- Whether negative cases cover what real users say, not only synthetic phrases;
- Whether the description has a cue that separates this skill from the closest alternative.

For a new skill, write and test the description before expanding the body. Use the trigger checks in [iteration-and-evaluation.md](iteration-and-evaluation.md). For wording rules and examples, see [instruction-craft.md](instruction-craft.md).

Weak: `Helps with skills.`
Strong: `Create, refactor, and evaluate Agent Skills... Do not use to execute an existing skill or perform a one-off task.`

## Harness compatibility

A harness is the agent runtime that discovers, loads, and runs skills. Examples include Claude Code, Codex CLI, and DeepSeek Harness.

Harnesses differ in capability. Before writing platform mechanisms, check:

- Whether subagents, hooks, tool permissions, or special frontmatter are supported;
- Whether `references/` is discovered and loaded;
- How file paths are resolved and whether relative paths are supported;
- Whether scripts can run and what the permission boundary is.

Do not assume that other harnesses support a mechanism because one harness does. When you cannot verify, choose the portable approach and state the unverified limitation.

## Follow project conventions

- Follow the target project's directory layout, naming, packaging, and distribution rules.
- Do not assume that this skill's own repository layout or tooling applies elsewhere.
- Keep runtime references relative and inside the skill. Do not point to absolute paths, other repositories, or local machine locations.
- Keep field names, types, and value domains for structured artifacts in one authoritative schema (for example, `schemas/`), and derive code and tests from it.
- Keep iteration records, evaluation output, and one-off research out of the distributed runtime surface.
- Remove or archive retired implementations instead of leaving them active.

## Complexity check

Before delivery, ask:

- Does every file have a clear purpose?
- Does any structure exist for a need that does not exist?
- Does `SKILL.md` make the main path clear and route the agent to required references before the relevant decision or action, with a read-when, plus a skip-when when over-reading is a risk?
- Are references routed by task rather than loaded by default?
- Could fewer components achieve the same result?

Delete what can be deleted. Structural complexity needs demonstrated capability value.
