# API Migration Note: Design Record

## Why this skill exists

Downstream teams kept asking what changed and in which order to act. A one-off answer per release did not survive a quarter, and the project instructions cannot carry the note structure.

## Decisions

- Impact before upgrade steps. A reader who stops after the first paragraph must still know whether they are affected. Rejected: an alphabetical endpoint list, which hides the impact.
- One step per breaking change. Rejected: a single migration script, because not every team can run it.
- Examples last: a call that already shows the change is easier to read after the steps.

## Open question

Whether old and new behavior belong in one table or two, for a change that renames a field.
