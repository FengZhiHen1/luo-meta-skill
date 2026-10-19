# Contributing

Thanks for helping improve Luo Meta Skill. This repository is the public distribution of the skill; the method is documented in `SKILL.md` and `references/`.

## What is useful

- A real request that triggered the wrong skill, or failed to trigger this one.
- A `description` that routes poorly, with the positive, negative, and neighboring cases.
- A reference that is unclear, duplicated, or missing a decision cue.
- A translation fix in `README.zh-CN.md`.

## Before a substantial change

Open an issue that states the problem, the affected file, and the expected behavior. Small fixes (typos, broken links, wording that does not change behavior) can go straight to a pull request.

## Development

There is no build step. Edit the Markdown files and check:

- Relative links resolve.
- Runtime guidance stays in English.
- `SKILL.md` keeps its frontmatter and the reference routing table.
- If behavior or installation changes, update both README files.
- If a description changes, test positive, negative, and neighboring cases in a real harness before claiming an improvement.

## Commit and pull request

- Use Conventional Commits, for example `docs: clarify trigger boundary`. PR titles follow the same format; the repository uses squash merge, so the PR title becomes the commit title.
- Describe the problem, the change, the verification, and the remaining risk.
- Link related issues with `Closes #123`.
- Disclose substantial AI assistance in the pull request description.
- Do not claim a test that was not run.

## Language

Runtime guidance is English. Issues and pull requests may be written in English or Chinese. Keep `README.md` and `README.zh-CN.md` in sync.

## Conduct

Be direct and respectful. Harassment, personal attacks, and disclosure of private information are not accepted.
