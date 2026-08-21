---
name: test-validation-planner
description: "Plan proportionate tests and validation for a feature, defect investigation, refactor, requirement, or documentation claim. Use when expected behavior, risks, existing coverage, and validation constraints need a reviewable test plan."
argument-hint: "Intended behavior, risks, and existing tests"
---

# Test and Validation Planner

## Purpose

Translate intended behavior and risk into concrete, observable validation steps. The result is a plan, not test execution or an approval decision.

## Procedure

1. State the behavior or claim being validated and its acceptance criteria.
2. Inspect relevant existing tests and identify coverage gaps.
3. Select unit, integration, regression, manual, or documentation checks proportionate to the risk.
4. Specify required test data, environment, expected result, and failure signal for every check.
5. Identify validation that cannot be completed and why.

## Output Format

```markdown
## Validation Plan

**Behavior or claim:** <description>

| ID | Validation type | Scenario | Setup or data | Expected result | Risk addressed |
| --- | --- | --- | --- | --- | --- |
| V-1 | Unit / Integration / Regression / Manual / Documentation | <scenario> | <setup> | <observable result> | <risk> |

**Existing coverage used:**
- <test path or validation source>

**Unvalidated risks:**
- <risk and reason>
```

## Boundaries

- Do not report validation as passed without execution evidence.
- Do not lower acceptance criteria to match an unverified implementation.
- Escalate missing environments, test data, or ownership decisions.