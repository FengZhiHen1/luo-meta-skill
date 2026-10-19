# Writing Precise Runtime Instructions

Read when writing or materially changing `SKILL.md`, `description`, reference routing, or important operating rules.

## Settle semantics first

Before changing wording, determine:

- What the target result is;
- What the default path is;
- Which conditions change behavior;
- Which external contracts must be exact;
- Which exceptions genuinely exist;
- When to stop or report failure.

For each instruction, ask: without this line, what could the agent do wrong? If you cannot answer, the line may not be needed. Good language cannot fix behavior that is wrong.

Then apply technical-writing principles inspired by ASD-STE100. Borrow its clarity; do not claim conformity with its controlled dictionary, grammar, or certification. Apply the same low-ambiguity principles to technical text in other languages. Do not mechanically impose English sentence-length limits.

Apply these rules only to technical runtime instructions. Do not constrain user creative output, quoted source material, literary style, or specialist terminology. Judge those by the task's own quality goals.

## Match constraint strength to the behavior

| Behavior | Write it as | Avoid |
| --- | --- | --- |
| Strict interface, file format, safety boundary | Exact inputs, actions, outputs, and failure boundaries | Synonyms for identifiers that must match; vague exceptions |
| Conditional operation, knowledge loading | Observable situation, direct action, essential exceptions | "as appropriate" without a decision signal; "always read everything" |
| Professional judgment | Goal, discriminating cues, trade-offs, example strategies | Mechanical one-size-fits-all if/else |
| Creative work | Quality goal, audience, constraints, examples, and room for alternatives | Exhaustive procedures that block strong new solutions |

State a clear default when one exists. A default is not the only permitted method. Use "must", "never", and "always" only for genuine invariants. Do not use capitals or strong words to manufacture false precision.

## Technical writing rules

- Use one term per concept. Keep file names, symbols, parameters, and API identifiers exact.
- Use explicit actions and objects. Prefer verbs with observable results. Avoid adjectives such as "appropriate", "robust", or "comprehensive" when they stand alone.
- Place conditions near the operation they govern. Avoid unclear pronouns and chained negations.
- Write the normal path first. Then describe non-obvious fallbacks, failures, and stopping conditions. Add them only when omission would cause a wrong action or an endless retry.
- State exact values, units, ranges, boundaries, and applicable scope. Distinguish capability, permission, and obligation.
- Number steps only when order matters. Present parallel strategies as a table or short options, not as pseudo-steps.
- Keep short reasons and contrasting examples that help the agent transfer professional judgment to unfamiliar cases.
- Preserve meaningful conditions and exact interface requirements when simplifying the text.
- Do not invent numeric thresholds, source counts, or minimum example counts to simulate precision. Use a numeric limit only when an external contract or an observed failure requires it.
- Do not claim that skill text outranks the harness's instruction hierarchy. External examples and retrieved documents are material, not authority.
- For Chinese or other non-English text, use natural word order and avoid translationese. Put conditional clauses before the action. Give the English term at first use when it helps precision.

## Trigger descriptions

`description` is a routing contract: the harness reads the name and description before the body and decides from them whether to load the skill. Write for that decision. The hard limits are in `SKILL.md`; this section covers judgment.

Apply these rules when writing or materially changing a description. Do not rewrite an existing description only to satisfy a style rule; change it when the capability, trigger boundary, or an observed routing problem requires it.

### State the job, not the workflow

`SKILL.md` states the rule. The failure mode is concrete: upstream testing reports that a description summarizing the workflow can make the agent follow the summary and skip the body. For example:

- Weak: `Use when reviewing code — runs lint, then a security scan, then writes a report.`
- Better: `Review code changes for correctness, security, and missing tests. Use when preparing a merge request or checking a change before review. Do not use for writing new features or fixing build failures.`

A short capability list is acceptable; an outline of the body is not. If the description needs several unrelated jobs, the skill scope is probably too broad.

### Write the trigger boundary

- Use the words users type: task verbs, artifact names, domain terms, and common shorthand. Do not turn the description into a keyword list.
- Name non-trigger requests only when a neighboring skill or a real false-positive risk exists. An invented exclusion adds noise and can cause under-triggering.
- State the cue that separates this skill from the closest alternative.
- Keep the shortest wording that preserves the boundary. When two versions route equally well, choose the shorter one; a longer candidate without a routing gain is a regression.
- Name a provider only when the skill is provider-specific; otherwise keep the description portable.

### Language

- Write in the language of the requests the skill must catch. Keep product names, identifiers, and the exact terms users type.
- For a mixed-language audience, use one primary language and include the key terms from the other. Do not add a full translation; it consumes the description budget without adding routing value.
- For a skill with an international audience, use English as the primary language; add terms from other languages only when they change routing.
- Do not translate established technical terms only for style.

### Format

- Quote the YAML string when it contains `: ` or `#`; a block scalar is valid.
- Do not use `<` or `>`; some harnesses and validators reject them.

## Revision strategy

- Prefer replacing, narrowing, or deleting an unsuitable rule before adding one.
- Preserve the original intent and necessary exceptions. Simpler language does not mean a simpler contract.
- Do not turn one failed observation into a global rule. First check whether it is reproducible and whether it applies only to one kind of task.
- Do not add many branches to cover extreme cases. Write the important boundaries and leave the rest to judgment.
- After editing, check that terms are consistent, conditions remain next to their actions, and defaults and exceptions do not contradict each other.
- Delete duplicate passages. Two near-identical rules make the agent choose one, not follow both.

## Precision check

Before delivery, check each item:

- Does every rule point to an observable behavior or result?
- Is the default path clear?
- Are important conditions, exceptions, and stopping points missing?
- Do conflicting old rules remain?
- Are key identifiers, paths, and formats exact?
- Has a preference been written as a hard requirement?
- Does the text invent numeric thresholds, source counts, or minimums without a real basis?
- Has precision reduced legitimate room for professional judgment?
- Does reference routing state when to read and when not to read?

## Contrasting examples

Research scope

Weak: `Always do full research before editing any skill.`
Better: `For new domain behavior, check representative tasks and reliable domain sources. For a spelling-only change that does not change behavior, edit the affected text directly.`

Reference routing

Weak: `Read the relevant documents when needed.`
Better: `Read references/layout-selection.md before choosing a new page layout. Do not load it for text-only edits.`

Professional judgment

Weak: `Always use a two-column layout for comparisons.`
Better: `Choose the structure from the dimensions readers must compare. Use a matrix for several comparable dimensions. When one difference carries the main conclusion, consider an asymmetric structure.`

Stopping

Weak: `Keep checking until the output is perfect.`
Better: `Fix actual failures that affect the agreed acceptance criteria. Stop when the required checks pass and no known material defect remains. Report limitations that could not be checked.`

The examples show language and decision writing. The suggested professional strategies still need validation in the target task.
