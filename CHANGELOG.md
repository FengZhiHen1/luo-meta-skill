# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `references/reference-routing.md`: routing contract, route formats, anti-patterns, and a three-task routing test.
- `references/skill-architecture.md`: `SKILL.md` body shape standard with five required questions, a minimal skeleton, shape-specific emphasis, and forbidden content.

### Changed

- `SKILL.md`, `skill-architecture.md`, and `instruction-craft.md` now treat routing as a decision: explicit default, read-when, and skip-when when over-reading is a risk.
- `SKILL.md` now uses a read-when/skip-when routing table and a stop/hand-back block; `instruction-craft.md` checks the five body questions.

## [0.1.0] - 2026-10-19

### Added

- Initial public release of the Luo Meta Skill.
- Description routing constraints: capability vs workflow, 1024-character limit, no angle brackets, no first person, conditional exclusions, and language by audience.
- References for research, architecture, instruction craft, and iteration.
- English and Simplified Chinese README.
