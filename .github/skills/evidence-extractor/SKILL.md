---
name: evidence-extractor
description: "Extract traceable engineering evidence from logs, test results, error messages, source code, configuration, and documentation. Use when an agent needs facts for a technical investigation, requirement, refactor, feature plan, or documentation review."
argument-hint: "Question to investigate and source locations"
---

# Evidence Extractor

## Purpose

Collect relevant facts without turning observations into conclusions. This skill provides the evidence base used by engineering agents.

## Procedure

1. State the investigation question and the sources that may answer it.
2. Read only the relevant source sections; preserve file paths, test names, log timestamps, versions, and commit identifiers when available.
3. Separate directly observed facts from inferred statements.
4. Identify missing or conflicting evidence.
5. Return the evidence record below.

## Output Format

```markdown
## Evidence Record

**Question:** <question>

| ID | Observed fact | Source | Relevance |
| --- | --- | --- | --- |
| E-1 | <fact> | <path, log timestamp, test, or URL> | <why it matters> |

**Conflicts or gaps:**
- <missing, contradictory, or inaccessible evidence>

**Inferences not yet confirmed:**
- <inference and supporting evidence IDs>
```

## Boundaries

- Do not claim a root cause, approve a change, or alter a source.
- Do not expose secrets found in logs or configuration; redact them and record only their location and type.
- Label inferences as unconfirmed until another agent or reviewer validates them.