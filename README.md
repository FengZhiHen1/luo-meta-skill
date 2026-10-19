# Luo Meta Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**An Agent Skill for designing, refactoring, and evaluating reusable Agent Skills.**

[English](README.md) | [简体中文](README.zh-CN.md)

> [!IMPORTANT]
> Early public release (`0.1.0`). Text, structure, and reference checks are complete; runtime behavior has not been evaluated across all hosts. See [Status](#status).

## Why this exists

Most weak skills do not fail because they lack prose. They fail because the scope is too broad, the `description` summarizes the workflow instead of the trigger boundary, the body is loaded too late, or the skill was never tested against real requests.

Luo Meta Skill is a method for those decisions. It helps an agent decide whether a skill is warranted, research the domain, design the runtime structure, write precise instructions, and verify the result without turning the project into a documentation pile.

## What it does

- **Decide whether a skill is warranted.** Distinguishes a reusable skill from a one-off task, a repository convention, or a deterministic check.
- **Research before writing.** Uses two anchors: representative tasks and capability gaps, plus systematic domain knowledge.
- **Design the runtime.** Covers scope, reference routing, scripts and assets, host compatibility, and the main path.
- **Write precise instructions.** Settles semantics first, matches constraint strength to behavior fragility, and treats the `description` as a routing contract.
- **Verify proportionately.** Uses trigger cases, real artifacts, before/after comparison, and honest reporting of what was not tested.

## Quick start

### Requirements

- An Agent Skills-compatible host that loads `SKILL.md` and can read relative Markdown references.
- No runtime, package manager, or API key. The skill has no scripts.

### Install

Clone the repository:

~~~bash
git clone https://github.com/FengZhiHen1/luo-meta-skill.git
~~~

Place the directory in the location your host uses for skill discovery, using the name `luo-meta-skill`. The exact path depends on the host. The skill uses only `SKILL.md` and Markdown references.

### Verify

Start a fresh agent session and ask:

> Create a skill for reviewing Terraform changes. Include trigger boundaries, reference routing, and a verification plan.

A working setup loads `luo-meta-skill`, classifies the task, and produces a `SKILL.md` with a scoped description and a verification plan. If the host lists available skills, confirm that `luo-meta-skill` appears.

If the skill does not load, check that the host read the `description` in `SKILL.md` and that the directory is in the host's skills path.

## Example: a description that routes

The `description` is the text most hosts read before deciding whether to load a skill. If it summarizes the workflow, the agent can follow the summary and skip the body.

Weak:

> Use when reviewing code — runs lint, then a security scan, then writes a report.

Better:

> Review code changes for correctness, security, and missing tests. Use when preparing a merge request or checking a change before review. Do not use for writing new features or fixing build failures.

The better version states the job and the boundary. It does not encode the sequence. The full rule set is in [SKILL.md](SKILL.md) and [references/instruction-craft.md](references/instruction-craft.md).

## What's inside

~~~text
luo-meta-skill/
├── SKILL.md
├── references/
│   ├── research-and-synthesis.md
│   ├── skill-architecture.md
│   ├── instruction-craft.md
│   └── iteration-and-evaluation.md
├── docs/
│   └── skill-design.md
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
└── LICENSE
~~~

Runtime files: `SKILL.md` and `references/`. `docs/` records design intent and source trade-offs. The remaining files are repository metadata.

## Design principles

- **Description is a routing contract.** The host reads the name and description before the body; trigger conditions belong there.
- **Capability over documentation volume.** A skill should change what the agent decides or does, not add files.
- **Shapes are starting points.** Procedure, knowledge, tool, judgment, and creative shapes; adapt them to the task.
- **Research with two anchors.** Representative tasks and capability gaps, plus systematic domain knowledge.
- **Verification proportional to risk.** Text checks for wording, artifacts for behavior, trigger cases for routing.
- **Host-neutral by default.** No provider-specific mechanisms unless the target host verifies them.
- **English runtime, any language for target skills.** The skill's own guidance is English; a target skill follows its audience.

## Compatibility

Luo Meta Skill is designed for hosts that implement the [Agent Skills specification](https://agentskills.io/specification): a `SKILL.md` with YAML frontmatter, progressive disclosure through `references/`, and relative paths.

It uses no scripts, hooks, subagents, provider-specific frontmatter, or network access. Behavior depends on the host's skill loader and model; runtime behavior has not been evaluated across all hosts.

## Status

- `0.1.0`, early public release.
- Text, structure, and reference checks are complete.
- Runtime behavior has not been evaluated across hosts.
- No CLI, evaluation platform, or governance system is included.
- Runtime guidance is in English. Target skills may be written in any language.

## Security

Do not report security problems in public issues. Follow [SECURITY.md](SECURITY.md).

## Contributing

Issues and pull requests are welcome in English or Chinese. Read [CONTRIBUTING.md](CONTRIBUTING.md) before a substantial change.

If a contribution is substantially AI-generated, disclose it in the pull request description. Do not claim tests that were not run.

## Acknowledgements

The method synthesizes public work on Agent Skills, including the [Agent Skills specification](https://agentskills.io/specification) and skill-authoring approaches from Sentry, OpenAI, Anthropic, Superpowers, Skillet, and Yao Meta Skill. [docs/skill-design.md](docs/skill-design.md#source-trade-offs) records what was adopted and what was not.

## License

[MIT](LICENSE) © 2026 FengZhiHen1
