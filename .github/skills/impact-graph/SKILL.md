---
name: impact-graph
description: 'Build a dependency graph (callers, callees, tests, and config references) for a given symbol, file, or module. Use when analyzing the blast radius of a refactoring change, understanding what a new feature will touch, or tracing how a failure propagated. Returns a structured dependency table.'
argument-hint: 'Symbol name, file path, or module to analyze'
tools: [search, read]
version: "1.0"
user-invocable: true
---

# Impact Graph

## What It Does

Given a symbol (function, class, variable), file path, or module name, builds a dependency graph showing who calls it (callers), what it calls (callees), which tests exercise it, and which config files reference it. This is the skill that makes refactoring and feature planning **bounded**.

## When to Use

- Refactoring Agent needs to know the blast radius before proposing a change
- Feature Agent needs to know which existing modules and tests a new feature will touch
- Debugging Agent needs to trace how a failure in module A propagated to module B
- Any time an engineer asks "if I change X, what else breaks?"

## When NOT to Use

- You only need to read one function → use `read_file` directly
- You need semantic (meaning-based) search → use `semantic-search`
- You are citing evidence → use `citation-extract`

## Procedure

1. **Identify** the target: a symbol name (function/class/variable), a file path, or a module name
2. **Find all references** using `vscode_listCodeUsages` to get callers and callees
3. **Search for tests** that import or reference the target using `grep_search` with patterns like:
   - `import.*<symbol>` / `from.*<module>`
   - `describe.*<symbol>` / `test.*<symbol>` / `it.*<symbol>`
4. **Search for config references** using `grep_search` in config directories:
   - `*.yaml`, `*.yml`, `*.json`, `*.toml`, `*.env` files referencing the symbol
5. **Categorize** each result:
   - **Direct** — will change if the target changes (callers that pass args, re-exports)
   - **Indirect** — may need a re-export or type-only update (barrel files, index files)
   - **Test** — test files that verify the target's behavior
   - **Config** — config files that reference the target by name
6. **Return** the structured impact table (see Output Format)

## Output Format

```markdown
### Impact Graph: `<symbol>` in `file:line`

#### Callers (who calls this)
| File | Line | Context | Direct / Indirect |
|------|------|---------|-------------------|
| `src/api/handler.ts` | 34 | `processOrder(payload)` | Direct |
| `src/api/index.ts` | 8 | `export { processOrder }` | Indirect (re-export) |

#### Callees (what this calls)
| File | Line | Context |
|------|------|---------|
| `src/payments/db.ts` | 12 | `saveOrder(order)` |
| `src/utils/logger.ts` | 5 | `log.info(...)` |

#### Tests
| File | Line | Test name |
|------|------|-----------|
| `tests/payments.test.ts` | 15 | "should retry on timeout" |
| `tests/payments.test.ts` | 42 | "should reject invalid payload" |

#### Config References
| File | Key | Value |
|------|-----|-------|
| `config/app.yaml` | `payment.retry_max` | `3` |

#### Summary
- **Files directly impacted:** N
- **Files indirectly impacted:** N
- **Tests affected:** N
- **Config files referencing target:** N
```

## Used By

| Agent | How |
|-------|-----|
| Refactoring Agent | Mandatory: builds the blast-radius table before proposing any change |
| Feature Agent | Identifies which existing modules/tests a new feature will touch |
| Debugging Agent | Traces how a failure propagated through a call chain |

## Notes

- This skill is **read-only** — it never modifies files
- Results depend on the codebase being statically analyzable (typed languages give better results)
- For dynamically-typed code (Python, JS), supplement with `grep_search` pattern matching
- Always cross-check with `semantic-search` for usage patterns static analysis might miss
