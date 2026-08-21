---
name: review-packager
description: "Package engineering findings into a concise, human-reviewable decision record with evidence, assumptions, risks, validation results, and out-of-scope items. Use before handing off feature plans, debugging investigations, documentation changes, refactoring proposals, or clarified requirements."
argument-hint: "Findings, evidence, proposed actions, and validation results"
---

# Review Packager

## Purpose

Create a consistent review artifact that lets engineers inspect reasoning, make decisions, and reject unsupported conclusions.

## Procedure

1. Gather only supported findings, linked evidence, assumptions, proposed actions, and validation results.
2. State the decision needed from the human reviewer.
3. Separate confirmed facts from hypotheses and explicitly state confidence.
4. Record risks, unresolved questions, and work intentionally excluded from the request.
5. Return the review package below.

## Output Format

```markdown
## Engineering Review Package

**Work item:** <title>
**Prepared by:** <agent name>
**Decision needed:** <approve, choose, clarify, or investigate>
**Confidence:** High / Medium / Low

### Summary
<concise, evidence-backed summary>

### Evidence
- <evidence ID or source link and relevance>

### Assumptions and hypotheses
- <item, status, and evidence>

### Proposed action
- <specific next action>

### Validation status
- <completed validation and result, or planned validation>

### Risks and open questions
- <item>

### Out of scope
- <item>
```

## Boundaries

- Do not hide uncertainty, failed checks, conflicting evidence, or missing inputs.
- Do not make the final approval decision on behalf of a human engineer.
- Do not include credentials, personal data, or other restricted content in the package.