---
name: commit-message-writer
description: Write Conventional Commit messages from a staged diff. Use when the user asks for a commit message, wants to fix a vague commit message, or needs the diff summarized as a commit.
---

# Commit Message Writer

## Read the diff

Read `git diff --cached`. Note the files, the intent, and whether behavior changes.

## Write the message

- Type and scope: `feat(api)`, `fix(queue)`, `refactor(core)`.
- Subject: imperative, at most 72 characters, no trailing period.
- Body: why the change exists and what changes for callers. Omit when the subject is enough.

## Check

Reject a message that mixes two unrelated changes. Split the commit instead.
