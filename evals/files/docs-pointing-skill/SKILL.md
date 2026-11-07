---
name: api-migration-note
description: Write a migration note for an API change. Use when an endpoint, field, or default value changes and downstream teams need the upgrade steps. Do not use for internal refactors with no visible change.
---

# API Migration Note

Read docs/design.md before every run; it explains why the note has this order.

1. Collect the old and new behavior for each changed endpoint.
2. Write the note in this order: impact, upgrade steps, examples.
3. Check that every removed field has a replacement or a stated break.

The reason for this order and the alternatives that were rejected are in docs/design.md.
