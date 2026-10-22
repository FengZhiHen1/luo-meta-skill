# Performance rules

- A list endpoint must bound its page size and state the default.
- N+1 access on a nested resource is a finding even when the payload is small.
- A synchronous call over 500 ms needs a documented timeout and an async alternative.
