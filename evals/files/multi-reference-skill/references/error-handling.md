# Error handling rules

- Every non-2xx response carries a stable machine-readable code.
- A 5xx must not leak stack traces or internal host names.
- Retries are safe only for idempotent methods; document retry semantics on the endpoint.
- Rate-limit responses carry a retry-after hint.
