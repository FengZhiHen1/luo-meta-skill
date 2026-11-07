---
name: dependency-audit
description: Audit a project's dependencies for outdated or risky versions. Use when checking a lockfile, planning an upgrade, or answering whether a dependency is still maintained. Do not use for installing packages or for a full security review.
---

# Dependency Audit

1. Read the lockfile and list direct dependencies with their current versions.
2. For each dependency, check the latest stable version and the last release date.
3. Rank findings by runtime impact, not by version lag.
4. Report: dependency, current version, latest version, risk, and the smallest safe upgrade.

Read references/risk-levels.md before assigning a risk level. Do not read it when the audit is limited to one dependency.
