---
name: migration-planner
description: Plan a schema migration: sequence the steps, choose a rollout strategy, and write the rollback plan. Use when the user asks how to migrate a live table, add a column without downtime, or roll back a failed migration.
---

# Migration Planner

## Decide

- Expand and contract, or a single change.
- Backfill in batches, or a one-shot statement.
- Rollback: reverse migration, or a restore point.

## Output

An ordered plan with verification at each step and a stop condition.
