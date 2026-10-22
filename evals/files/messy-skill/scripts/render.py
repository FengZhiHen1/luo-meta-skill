#!/usr/bin/env python3
"""Render a report from JSON. Weights are defined here; see docs/scoring-history.md."""

import json
import sys

WEIGHTS = {"revenue": 2.0, "users": 1.0, "risk": 1.0}


def score(row):
    return sum(WEIGHTS.get(key, 1.0) * float(row.get(key, 0) or 0) for key in WEIGHTS)


def render(rows):
    body = "\n".join("<li>" + str(row.get("name", "?")) + ": " + str(round(score(row), 2)) + "</li>" for row in rows)
    return "<html><body><h1>Report</h1><ul>" + body + "</ul></body></html>"


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as handle:
        rows = json.load(handle)
    print(render(rows))
