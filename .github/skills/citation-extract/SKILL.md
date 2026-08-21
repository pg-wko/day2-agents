---
name: citation-extract
description: 'Extract exact quotes with file:line or section references from source code, logs, spec documents, and error messages. Use when an agent needs to cite evidence for a claim, requirement, or hypothesis. Ensures every output is traceable and reviewable.'
argument-hint: 'The file, log, or document to extract citations from'
user-invocable: true
---

# Citation Extract

## What It Does

Given a source (file, log, specification document, or error message), extracts the exact text that supports a claim and attaches a precise citation in `source:line` or `source §section` format. This is the skill that makes all agent outputs **reviewable**.

## When to Use

- Requirements Agent needs to cite the spec section a requirement came from
- Documentation Agent needs to cite `file:line` for an architectural claim
- Debugging Agent needs to cite the exact log line that supports a hypothesis
- Feature Agent needs to cite the code module a new feature will affect

## When NOT to Use

- You are generating new content (a diff, a test plan) rather than citing existing content
- The source is a conversation or chat — only cite durable artifacts (files, logs, docs)

## Procedure

1. **Identify** the source artifact: file path, log file, spec document, or pasted text
2. **Read** the relevant section with `read_file` (for files) or parse the provided text
3. **Locate** the exact lines or paragraphs that contain the supporting evidence
4. **Format** the citation:
   - Source code / logs → `file:line` (e.g., `src/payments/retry.ts:55`)
   - Spec documents / wikis → `document §section` (e.g., `PRD-v2 §3.2.1`)
   - Error messages → `log_file:line` (e.g., `app.log:147`)
5. **Quote** the exact text — no paraphrasing, no summarizing
6. **Return** a citation block (see Output Format)

## Output Format

```markdown
### Citation

> `<exact quoted text from the source>`

**Source:** `file_or_document:line_or_section`
```

For multiple citations:

```markdown
### Evidence

1. > `<exact quote>` — `src/payments/retry.ts:55`
2. > `<exact quote>` — `app.log:147`
3. > `<exact quote>` — `PRD-v2 §3.2.1`
```

## Used By

| Agent | How |
|-------|-----|
| Requirements Agent | Cite the spec section each requirement is extracted from |
| Documentation Agent | Cite `file:line` for every architectural claim |
| Debugging Agent | Cite exact log lines and source locations for each hypothesis |
| Feature Agent | Cite the requirement and source code that justify each test case |

## Notes

- **Never paraphrase** in the quote block — the text between backticks must be verbatim
- If the source is too long to quote in full, quote the critical sentence and cite the broader section
- This skill is **read-only** — it never modifies files
- The citation format is designed for human review: an engineer should be able to `Ctrl+G` to the line and verify
