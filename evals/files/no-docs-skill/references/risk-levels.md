# Risk Levels

- critical: a known vulnerability in a dependency the service runs in production.
- high: a major version lag on a dependency that ships in the request path.
- medium: a major version lag elsewhere, or an unmaintained dependency.
- low: a minor or patch lag with no security note.

A dependency counts as unmaintained when its last release is older than two years.
