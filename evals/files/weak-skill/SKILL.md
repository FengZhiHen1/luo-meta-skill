---
name: release-notes-helper
description: Use when producing release documentation artifacts — consolidates commit metadata into the standardized release communication unit, applies the house style profile, and hands off to the distribution channel owner.
---

# Release Notes Helper

## Position in the pipeline

This skill occupies the release documentation slot between merge freeze and distribution. It consumes
commit metadata and emits the standardized release communication unit.

## Operating model

1. Ingest commit metadata from the repository of record.
2. Apply the house style profile to the consolidated metadata set.
3. Emit the release communication unit for channel distribution.

## Conventions

- Terminology follows the documentation style profile.
- Artefacts inherit the release window identifier.
- Exceptions route to the release manager for disposition.

## Resources

The format guide is stored in the references directory.
