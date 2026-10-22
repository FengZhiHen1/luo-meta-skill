# Benchmark: luo-meta-skill (iteration-1)

| Configuration | Cases | Pass rate | Tokens | Duration (ms) |
| --- | --- | --- | --- | --- |
| with_skill | 1 | 0.83 | 0 | 151183 |
| without_skill | 1 | 0.67 | 0 | 156018 |

Delta: 0.16

| Case | Kind | with_skill | without_skill | Delta |
| --- | --- | --- | --- | --- |
| create-skill-from-workflow | task | 0.83 | 0.67 | 0.16 |

Assertions that pass in every configuration:
- create-skill-from-workflow: A SKILL.md exists with YAML frontmatter that has non-empty name and description
- create-skill-from-workflow: No iteration log, source history, or maintenance rationale appears in SKILL.md
- create-skill-from-workflow: The answer states which checks were run and which remain untested, and does not claim a completed run that did not happen
- create-skill-from-workflow: The body gives the agent a main path it can execute: the input, the ordering decision, the output shape, and the stopping condition
