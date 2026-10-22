---
name: report-builder
description: Use when building reports. Read the docs, choose a template, run the render script, then check the output against the checklist in references/quality.md. The workflow is: gather data, normalize it, score it, render it, review it, publish it.
---

# Report Builder

## Purpose

This skill builds reports. Reports matter because readers need structure.

## Background

This skill was written during the 2024 reporting migration. Version 0.1 handled only CSV input. Version 0.2
added Excel support after the finance team asked for it. Version 0.3 split the renderer out.

## Overview

1. Gather data.
2. Normalize it.
3. Score it.
4. Render it.
5. Review it.
6. Publish it.

## Details

### Data

Data comes from CSV or Excel. Ask the user for the file. If the user has no file, ask again.

### Normalization

Normalize the data. Column names should be consistent. Handle missing values somehow.

### Scoring

Score each row. The scoring model is described in docs/scoring-history.md and was changed twice.

### Rendering

Run scripts/render.py. It takes a JSON file and produces an HTML report. Parameters are documented in
the script itself; read the source if you need them.

### Review

Check the output. Use the checklist.

### Publishing

Publish the report. Ask the user where to publish it.

## Notes

- The old Excel path is kept for compatibility.
- If the renderer fails, try again.
- Templates live in docs/templates/ (see docs/templates-notes.md for why there are two copies).
- For questions, see docs/faq.md.
