# Reference Routing

Read when designing, reviewing, or repairing the routing between `SKILL.md` and its `references/` files.

Routing is a decision, not a catalog. A file index answers "what is in this directory?" Routing answers "should I read this file now?"

## Contract

- The default path must work without reading a reference. State that default before the routes.
- Put one routing block in `SKILL.md`, after the main path and before the first decision that may need a reference.
- Every route has two required parts and one optional part:
  - **Read when** (required): an observable condition or a point in the task.
  - **File** (required): a relative path inside the skill, usually `references/<name>.md`.
  - **Skip when** (optional): the condition under which reading the file would waste context. Include it when over-reading is a real risk.
- Route by decision, action, or timing. "Before choosing a layout" is a route; "Layout" is a topic.
- One reference per decision. If two files are always read together, merge them or state their order.
- If a reference is always read, move its content into `SKILL.md`. If it is never read, delete it.

## Format

Use the smallest format that keeps the decision clear.

One route:

```markdown
Before choosing a page layout, read `references/layout-selection.md`. Skip it for text-only edits.
```

Two to five routes:

```markdown
Default: the main path needs no reference.

| Read before / when | File | Skip when |
| --- | --- | --- |
| Choosing a page layout | `references/layout-selection.md` | Text-only edits |
| The API returns a non-200 status | `references/api-errors.md` | The request succeeded |
```

Six or more routes: group them by decision point. If the block still does not fit, the skill may be too broad; narrow the scope before adding a router file. A router file is a last resort, not the default for a long list. If one is necessary, `SKILL.md` must state when to open it and what the default path is; the router is the single routing authority.

Keep conditions short. A table with long topic descriptions is a catalog, not routing.

## Placement and paths

- Keep the routing block near the main path, not at the bottom.
- Do not repeat the same route in several places. If a step needs a pointer, keep the full route in the routing block and add only a short pointer at the step.
- Use relative paths. Keep knowledge references flat: `references/foo.md`, not `references/foo/bar.md`. Assets and scripts may use their own layout.
- Give each reference file an opening `Read when ...` line that matches the route. Add `Do not read when ...` when the skip condition matters.

## Anti-patterns

- **Topic index**: `| gh commands | references/gh-cli.md |` without a condition or timing.
- **File list**: `See references/a.md, b.md, and c.md for details.`
- **Vague routing**: "Read the relevant documents when needed", "load as needed", "see references/ for details."
- **Nested knowledge**: `references/topic/file.md` when a flat file would work.
- **Router to router**: `SKILL.md` sends the agent to a file that only lists other files, without a default or a reason to open it.
- **No skip condition**: every route says "read when relevant", so the agent reads everything.
- **Duplicate routes**: the same file is routed from three places with different conditions.
- **Orphan reference**: a file exists but no route points to it.
- **Always-read reference**: a file that every task needs is not a reference; move it into `SKILL.md`.

## Routing test

Use three representative tasks:

1. The default task, which should need no reference.
2. A branch task that should read exactly one reference.
3. A neighboring task that should read none of the references.

Ask a reader who did not write the skill, or walk the three tasks as a new reader, which file they would read and which they would skip. If they cannot answer without opening the files, the condition is not observable or the route is missing. Fix the route, not the reader.

Then check:

- Every reference file is reachable from `SKILL.md` exactly once.
- Every route's file exists and is at the expected depth.
- Every reference file's opening `Read when` line matches its route.
- The default path does not require a reference.

## Checklist

- [ ] The default path is stated and needs no reference.
- [ ] One routing block, near the main path.
- [ ] Every route has a read-when, a file, and a skip-when when over-reading is a risk.
- [ ] Routes use decisions or timing, not topics.
- [ ] Knowledge references are flat and relative.
- [ ] No duplicate, orphan, or always-read references.
- [ ] Three-task routing test passes.
