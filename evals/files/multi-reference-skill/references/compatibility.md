# Compatibility rules

- Removing a response field breaks clients that read it; deprecate first.
- Adding a required request field breaks clients that omit it.
- Changing a field type is a breaking change even when the JSON shape looks the same.
- Widening an enum is safe; narrowing it is not.
