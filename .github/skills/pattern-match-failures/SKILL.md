---
name: pattern-match-failures
description: 'Match a new failure (error message, stack trace, or log signature) against a library of known historical root causes. Use when debugging a failure to check if it matches a previously seen and resolved issue. Returns ranked matches with similarity scores and known root causes.'
argument-hint: 'Error message, stack trace, or failure signature to match'
tools: [search, read]
version: "1.0"
user-invocable: true
---

# Pattern Match Failures

## What It Does

Given a new failure (error message, stack trace, or test failure signature), normalizes it into a failure signature and matches it against a library of known historical failures. Returns ranked matches with similarity scores and the known root cause for each match.

## When to Use

- Debugging Agent receives a new failure and wants to check if it's a known issue
- An engineer asks "have we seen this error before?"
- A test regression appears and you want to check if the same failure was previously debugged

## When NOT to Use

- You need to search the codebase for a concept → use `semantic-search`
- You need to cite a source → use `citation-extract`
- You need to analyze blast radius → use `impact-graph`

## Procedure

1. **Receive** a failure artifact: error message, stack trace, or test failure output
2. **Normalize** the failure into a signature:
   - Strip variable values (timestamps, IDs, memory addresses, file paths, line numbers)
   - Keep the error class, message template, and top 3 stack frames
   - Example: `TypeError: Cannot read property 'id' of undefined at processOrder (src/payments/service.ts:42)` → signature: `TypeError: Cannot read property '{prop}' of undefined at processOrder ({file})`
3. **Search** the failure library (stored as `.github/failures/` markdown files, or any configured knowledge base) using `grep_search` and `read_file`
4. **Score** each candidate match:
   - **High** — same error class + same message template + ≥1 matching stack frame
   - **Medium** — same error class + similar message template
   - **Low** — same error class only, or similar message but different error class
5. **Return** ranked matches with the known root cause and resolution (see Output Format)

### Failure Library Format

Historical failures are stored as markdown files in `.github/failures/`:

```
.github/failures/
├── F-001-off-by-one-retry.md
├── F-002-null-pointer-in-handler.md
└── F-017-timeout-in-db-pool.md
```

Each file contains:
```markdown
# F-017: <title>
- **Signature:** `TimeoutError: connection pool exhausted ({db}) at getPool ({file})`
- **Root cause:** DB connection pool max size was set to 5; under load, connections were not released
- **Fix:** Increased pool max to 20 and added connection release in finally block
- **Last seen:** 2025-11-03
- **Related files:** `src/db/pool.ts`, `config/db.yaml`
```

## Output Format

```markdown
### Pattern Match Results: "<normalized signature>"

#### Normalized Signature
`<error_class>: <message template> at <top_stack_frame>`

#### Matches

| Rank | Match ID | Similarity | Known root cause | Last seen |
|------|----------|-----------|-----------------|-----------|
| 1 | F-017 | **High** | DB pool exhaustion; connections not released | 2025-11-03 |
| 2 | F-003 | **Medium** | Similar timeout, but in HTTP client not DB | 2025-10-15 |

#### Best Match Detail

**F-017: <title>**
- **Signature:** `<signature>`
- **Root cause:** <description>
- **Fix applied:** <description>
- **Related files:** `<files>`
- **Source:** `.github/failures/F-017-timeout-in-db-pool.md`

#### Recommendation
If similarity is **High**, investigate the known root cause first.
If similarity is **Medium** or **Low**, treat as a new failure but keep this match as a reference.
```

## Used By

| Agent | How |
|-------|-----|
| Debugging Agent | First step: check if the failure is a known issue before hypothesizing |
| Feature Agent | Verify that a new feature's test cases don't duplicate known failure patterns |

## Notes

- This skill is **read-only** — it never modifies files
- The failure library grows over time as the team debugs new issues
- If no matches are found, this is a **new** failure — the Debugging Agent should narrate the triage and recommend storing a new entry in `.github/failures/`
- Normalization is critical: always strip variable values before matching
