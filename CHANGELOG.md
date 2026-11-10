# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Every skill now carries a design record under its own `docs/`: why the skill exists, scope and non-goals, and for each non-obvious rule the reason plus the alternative that was rejected. A small skill may record only its core design principle.
- `docs/` ships with the skill directory. The harness never loads it during a task, and runtime files must not point to it or restate it.
- Three eval cases with fixtures: a skill with no design record, a runtime file that points into `docs/`, and one principle restated across three files.
- `references/test-set-design.md`: two-question framing (necessity and quality), case families, prompt and fixture design, the assertion discriminating test, trigger and pressure cases, holdout, the default case format, and mapping for foreign case formats.
- `references/benchmark-runs.md`: executor preconditions and refusal rule, run layout, isolation rules, capture, repetitions, three grading layers, weak-assertion and necessity reading, and reporting rules.
- `references/eval-audit.md`: how to judge whether a case, a set, or a measured result can support its claim, including anchor, discrimination, baseline validity, coverage, author bias, instrument drift, and the conclusion-strength table.
- `source` field on cases (`real`, `derived`, `synthetic`) with a provenance note; `test-set-design.md` now requires every case to be anchored in a real task requirement, allows an authored prompt, and forbids invented difficulty or hints.
- `benchmark-runs.md` gains an evidence-strength table; a delta inside the observed spread is reported as no difference, and synthetic-only sets cannot support a necessity claim.
- `scripts/check_evals.py`: validates a case file against `schemas/evals.schema.json`, checks fixture paths, duplicate ids, and trigger-case consistency. Standard library only.
- `scripts/summarize_runs.py`: aggregates an iteration into `benchmark.json` and `benchmark.md` with with-skill versus baseline delta, non-discriminating cases, and weak assertions. Standard library only.
- `schemas/evals.schema.json` and `schemas/results.schema.json`: authoritative shape of the case file and the run result files; the scripts read them instead of restating field rules.
- `evals/`: the skill's own test set with six cases and fixtures, covering skill creation, non-skill decisions, weak-skill diagnosis, description boundaries, research-to-runtime, and verification under delivery pressure.
- `references/reference-routing.md`: routing contract, route formats, anti-patterns, and a three-task routing test.
- `references/skill-architecture.md`: `SKILL.md` body shape standard with five required questions, a minimal skeleton, shape-specific emphasis, and forbidden content.

### Changed

- `description` now covers building a skill test set and running with-skill and without-skill comparisons.
- `SKILL.md` routes test-set design and benchmark runs to the new references, adds `evals/` to the runtime content, and requires an independent executor for measured claims.

### Changed

- `SKILL.md`, `skill-architecture.md`, and `instruction-craft.md` now treat routing as a decision: explicit default, read-when, and skip-when when over-reading is a risk.
- `SKILL.md` now uses a read-when/skip-when routing table and a stop/hand-back block; `instruction-craft.md` checks the five body questions.
- `references/skill-architecture.md` gains a directory and file-template contract section: one dedicated carrier per structural contract, carrier chosen by contract type, a single authoritative copy, routing before the producing step, and the threshold for creating the file at all.
- `SKILL.md` states that a required output tree or file template gets its own file and a routing entry instead of an inline copy.
- Own test set: a case whose output tree and file structure are fixed, and the counter-case whose one-line path must not create a file.
- `SKILL.md` makes the design record mandatory, states that `docs/` ships but is never loaded, and requires merging a rule left stated in more than one file before delivery.
- `instruction-craft.md` requires one authoritative statement per rule, cross-file duplicate removal, and a duplicate check in the precision list.
- `skill-architecture.md` replaces "Specifications and design documents" with "Design record in docs/" and routes the record as a shipped, never-loaded component.
- README, README.zh-CN, and the skill's own design record describe the new contract.
- `skill-architecture.md` and `reference-routing.md` now default knowledge references to flat, one level from `SKILL.md`, and allow a subdirectory such as `references/domains/` only when a flat file would not work.

## [0.1.0] - 2026-10-19

### Added

- Initial public release of the Luo Meta Skill.
- Description routing constraints: capability vs workflow, 1024-character limit, no angle brackets, no first person, conditional exclusions, and language by audience.
- References for research, architecture, instruction craft, and iteration.
- English and Simplified Chinese README.
