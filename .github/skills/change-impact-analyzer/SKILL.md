---
name: change-impact-analyzer
description: "Analyze engineering change impact across source code, tests, configuration, interfaces, dependencies, and documentation. Use when planning a feature, investigating a failure, preparing docs, or proposing a behavior-preserving refactor."
argument-hint: "Change description or failure signature"
---

# Change Impact Analyzer

## Purpose

Identify artifacts likely to be affected by a proposed change or failure while making uncertainty visible.

## Procedure

1. Capture the proposed change or failure signature and its known entry point.
2. Trace direct references, callers, dependencies, configuration consumers, tests, and user-facing documentation.
3. Classify each artifact as directly affected, indirectly affected, or requiring manual inspection.
4. Explain the dependency path and confidence for each classification.
5. Return the impact record below.

## Output Format

```markdown
## Impact Record

**Subject:** <change description or failure signature>

| Artifact | Classification | Dependency path | Confidence | Required action |
| --- | --- | --- | --- | --- |
| <path or interface> | Direct / Indirect / Manual | <how it connects> | High / Medium / Low | <inspect, update, test, or none> |

**Potential interface or configuration risk:**
- <risk>

**Manual inspection required:**
- <artifact and reason>
```

## Boundaries

- Do not modify files or infer runtime behavior from static references alone.
- Do not mark an artifact unaffected when it could not be inspected.
- Escalate ambiguous dependency paths for engineering review.