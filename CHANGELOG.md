# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `references/test-set-design.md`: two-question framing (necessity and quality), case families, prompt and fixture design, the assertion discriminating test, trigger and pressure cases, holdout, the default case format, and mapping for foreign case formats.
- `references/benchmark-runs.md`: executor preconditions and refusal rule, run layout, isolation rules, capture, repetitions, three grading layers, weak-assertion and necessity reading, and reporting rules.
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

## [0.1.0] - 2026-10-19

### Added

- Initial public release of the Luo Meta Skill.
- Description routing constraints: capability vs workflow, 1024-character limit, no angle brackets, no first person, conditional exclusions, and language by audience.
- References for research, architecture, instruction craft, and iteration.
- English and Simplified Chinese README.
