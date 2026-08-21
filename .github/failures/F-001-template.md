# F-NNN: <failure title>

> **Copy this template to create a new failure entry.** Name the file `F-NNN-short-description.md` (e.g., `F-017-timeout-in-db-pool.md`). Fill in all fields below.

---

- **Signature:** `<error_class>: <message template with {placeholders}> at <top_stack_frame>`
- **Root cause:** <one-paragraph description of the actual root cause>
- **Fix applied:** <what was changed to resolve the issue>
- **Last seen:** <YYYY-MM-DD>
- **Related files:** `<file1>`, `<file2>`
- **Related tests:** `<test_file:line>` (if applicable)

## Error Signature (normalized)

```
<error_class>: <message with {variables} stripped> at <function_name> ({file})
```

## Notes

<Any additional context: how it was diagnosed, what experiments confirmed the root cause, or links to PRs/tickets.>
