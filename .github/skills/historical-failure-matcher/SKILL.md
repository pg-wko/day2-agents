---
name: historical-failure-matcher
description: "Match a current engineering failure against historical incidents, bug reports, postmortems, fixes, and known limitations. Use when investigating errors, logs, test failures, stack traces, or requirement risks that may resemble prior failures."
argument-hint: "Current failure signature and historical record locations"
---

# Historical Failure Matcher

## Purpose

Find relevant prior incidents without assuming that a similar-looking failure has the same cause.

## Procedure

1. Normalize the current failure into searchable signals: error text, stack frames, environment, affected component, and time window.
2. Search the supplied historical records for matching signals.
3. Compare each candidate incident with the current evidence, including meaningful differences.
4. Rank candidates based on explicit matching evidence rather than title similarity alone.
5. Return the match record below.

## Output Format

```markdown
## Historical Match Record

**Current signature:** <error, symptom, or risk>

| Rank | Prior incident | Matching evidence | Important differences | Confidence | Prior remediation |
| --- | --- | --- | --- | --- | --- |
| 1 | <record link or ID> | <facts> | <facts> | High / Medium / Low | <summary or link> |

**Conclusion:** <similarity finding, not a root-cause claim>

**Records not available:**
- <source and reason>
```

## Boundaries

- Never state that a historical fix applies until current evidence supports it.
- Do not disclose incident details that are restricted to the requesting context.
- Do not treat missing historical records as evidence that the failure is new.