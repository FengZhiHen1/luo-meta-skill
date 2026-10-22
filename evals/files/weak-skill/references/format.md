# Release Note Format

Use a heading per version, then grouped sections: Added, Changed, Fixed, Removed.
Each entry starts with the affected surface, then the behavior change.

## Version heading

```text
## 1.4.0 - 2026-03-02
```

## Entry shape

```text
- API: `POST /sessions` now rejects expired tokens with 401 instead of 500.
```

## Exclusions

Internal refactors with no user-visible behavior stay out of the notes.
