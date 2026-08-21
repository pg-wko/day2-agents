---
name: semantic-search
description: 'Find files, code snippets, and documentation by semantic meaning rather than exact keyword match. Use when searching for concepts like "retry logic", "authentication middleware", or "where is the database connection configured". Returns ranked results with file paths and relevance scores.'
argument-hint: 'What to search for (concept or natural-language query)'
tools: [search, read]
version: "1.0"
user-invocable: true
---

# Semantic Search

## What It Does

Given a natural-language query, finds files and code snippets whose **meaning** matches — not just files containing the exact keywords. Uses embedding-based similarity over the codebase to rank results.

## When to Use

- An engineer asks "where is the retry logic?" (no exact filename known)
- An agent needs to locate modules relevant to a feature before reading them
- Debugging needs to find all code paths that handle a specific error category
- Refactoring needs to find all call sites of a concept (not just a symbol name)

## When NOT to Use

- You know the exact symbol name → use `grep` / `vscode_listCodeUsages` instead
- You need the definition of a specific function → use `read_file` directly
- You need all references to a known identifier → use `vscode_listCodeUsages`

## Procedure

1. **Receive** a natural-language search query (e.g., "exponential backoff retry")
2. **Expand** the query with synonyms and related terms:
   - "retry" → "backoff", "reconnect", "re-attempt", "resilience"
   - "authentication" → "auth", "login", "token", "session"
3. **Search** the codebase using `grep_search` with regex alternation of the expanded terms
4. **Read** top candidate files (5–10) with `read_file` to assess true relevance
5. **Rank** results by relevance: direct definition > usage > mention in comment > test reference
6. **Return** a ranked list with `file:line`, a one-line description, and a relevance score (High/Medium/Low)

## Output Format

```markdown
### Semantic Search Results: "<query>"

| Rank | File | Lines | Relevance | Description |
|------|------|-------|-----------|-------------|
| 1 | `src/payments/retry.ts` | 42-89 | **High** | Exponential backoff with jitter — core retry loop |
| 2 | `src/utils/http.ts` | 120-145 | **Medium** | Generic HTTP retry wrapper, delegates to retry.ts |
| 3 | `tests/retry.test.ts` | 8-60 | **Low** | Test coverage for retry logic |
```

## Used By

| Agent | How |
|-------|-----|
| Documentation Agent | Find files that answer an engineer's question |
| Debugging Agent | Locate the code referenced in a stack trace |
| Refactoring Agent | Find all usage patterns of the target symbol |
| Feature Agent | Understand existing architecture before proposing a feature |

## Notes

- Results are best-effort; always follow up with `read_file` to confirm relevance
- If no results match, broaden the query or fall back to exact symbol search
- This skill is **read-only** — it never modifies files
