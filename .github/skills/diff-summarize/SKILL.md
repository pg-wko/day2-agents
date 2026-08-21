---
name: diff-summarize
description: 'Produce a human-readable summary of a code diff with risk annotations, breaking-change flags, and coverage impact. Use when the Refactoring Agent proposes a change, or when an engineer needs a review-friendly overview of a diff. Returns a structured diff summary with risk assessment.'
argument-hint: 'The diff or changed files to summarize'
user-invocable: true
---

# Diff Summarize

## What It Does

Takes a code diff (unified diff text, or a list of changed files with before/after content) and produces a structured, human-readable summary with risk annotations. This is the skill that makes all refactoring output **reviewable**.

## When to Use

- Refactoring Agent has drafted a change and needs to present it for human review
- An engineer asks "what does this diff do and what are the risks?"
- A PR review needs a quick risk assessment before deep-reading the diff

## When NOT to Use

- You need to find where code is → use `semantic-search`
- You need to analyze blast radius → use `impact-graph`
- You need to match a failure → use `pattern-match-failures`

## Procedure

1. **Receive** the diff: either unified diff text or a list of `{file, before, after}` items
2. **Classify** each change:
   - **Added** — new code added
   - **Removed** — existing code deleted
   - **Modified** — existing code changed
   - **Moved** — code moved without semantic change (e.g., extraction)
3. **Analyze** each change for risks:
   - **Breaking change** — signature change, removed public API, changed return type
   - **Side effect** — changes to I/O, network, DB, state mutation
   - **Test gap** — changed code with no test coverage
   - **Style/No risk** — rename, formatting, comment
4. **Estimate** coverage impact:
   - Compare lines changed against known test files (cross-ref with `impact-graph` results if available)
   - Flag any changed file with no corresponding test file
5. **Return** the structured summary (see Output Format)

## Output Format

```markdown
### Diff Summary

#### Changes at a Glance
| File | Change type | Lines changed | Risk |
|------|-------------|---------------|------|
| `src/payments/service.ts` | Modified | +12 -5 | Medium |
| `src/payments/handler.ts` | Added | +30 | Low |
| `tests/payments.test.ts` | Modified | +8 | None |

#### Detailed Changes

##### `src/payments/service.ts` (Modified — Medium risk)
- **What changed:** Retry backoff logic extracted from `processOrder` into `retryWithBackoff`
- **Breaking change:** No — `processOrder` signature unchanged
- **Side effects:** New function `retryWithBackoff` uses `setTimeout` (async, same as before)
- **Test coverage:** `tests/payments.test.ts` covers the extracted function ✅

##### `src/payments/handler.ts` (Added — Low risk)
- **What:** New HTTP handler delegates to `processOrder`
- **Breaking change:** No
- **Test coverage:** No test file for `handler.ts` yet ⚠️

#### Risk Assessment
| Risk | Severity | Mitigation |
|------|----------|------------|
| No test for new `handler.ts` | Medium | Add test before merge |
| `retryWithBackoff` changes timing | Low | Backoff values match original; verify with integration test |

#### Coverage Impact
- **Files changed with tests:** 1 ✅
- **Files changed without tests:** 1 ⚠️ (`src/payments/handler.ts`)
- **Estimated coverage delta:** -2% (new untested file)

#### Review Checklist
- [ ] Breaking changes? No
- [ ] All changed files have tests? No — `handler.ts` needs tests
- [ ] Side effects reviewed? Yes — timing unchanged
- [ ] Ready to merge? After adding handler tests
```

## Used By

| Agent | How |
|-------|-----|
| Refactoring Agent | Mandatory: produces the reviewable diff summary before human approval |
| Requirements Agent | Summarizes how a spec change impacts implementation (when applicable) |

## Notes

- This skill is **read-only** — it never applies diffs, only summarizes them
- The diff must already exist (drafted by the Refactoring Agent or provided as a PR diff)
- Risk severity scale: **None** < **Low** < **Medium** < **High**
- Always cross-reference with `impact-graph` when available for richer blast-radius context
