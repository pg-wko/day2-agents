# AI Engineering Team — 5 Specialist Agents & 5 Reusable Skills

> **Design principle:** Reusable · Reviewable · Bounded
>
> Each agent has a **specific engineering responsibility** — this is not a generic chatbot. Every agent output includes citations (`file:line` or `section`) so a human can verify every claim. Every skill is shared across multiple agents.

---

## Repository Structure (`.github` convention)

```
.github/
├── agents/
│   ├── requirements.agent.md      # Extract testable requirements from specs
│   ├── documentation.agent.md     # Map repos, answer "where is X" with citations
│   ├── debugging.agent.md         # Triage failures, rank root-cause hypotheses
│   ├── refactoring.agent.md       # Propose reviewable diffs with blast-radius analysis
│   └── feature.agent.md           # Turn requirements into testable feature plans
├── skills/
│   ├── semantic-search/SKILL.md       # Find code/docs by meaning, not keywords
│   ├── citation-extract/SKILL.md      # Pull exact quotes with file:line / section refs
│   ├── impact-graph/SKILL.md          # Build caller/callee/test dependency graph
│   ├── pattern-match-failures/SKILL.md # Match new failures against known root causes
│   └── diff-summarize/SKILL.md        # Produce reviewable diff summaries with risks
└── failures/                         # (optional) Historical failure library for pattern-match
    └── F-001-template.md
```

---

## The 5 Specialist Agents

| # | Agent | Responsibility | Bounded By |
|---|-------|---------------|------------|
| 1 | **Requirements Agent** | Extract testable requirements from specs, flag ambiguity | Reads docs only; never writes code or tests |
| 2 | **Documentation Agent** | Answer "where is X / what does Y do" with cited evidence | Read-only; every answer must have a citation |
| 3 | **Debugging Agent** | Triage failures (logs, errors, validation results), match against history, rank hypotheses | Never claims "fixed"; outputs hypotheses + next experiment |
| 4 | **Refactoring Agent** | Propose safe diffs with blast-radius and risk assessment | No direct writes; blocks for human approval before applying |
| 5 | **Feature Agent** | Turn approved requirements into feature plans + test cases | No production code; outputs feature → TCDs → test cases |

### Engineering Workflow

```
Spec/PRD ──▶ Requirements Agent ──▶ REQ-001, REQ-002, ...
                                        │
                                        ▼
                                   Feature Agent ──▶ Feature plan + TCDs + test cases
                                        │                              │
                                        ▼                              ▼
              ┌─────────────────────────────────────────────────┐
              │              Codebase (existing)                  │
              └─────────────────────────────────────────────────┘
                         │                              │
                         ▼                              ▼
              Documentation Agent              Refactoring Agent
              (answers "where is X")           (proposes diff, awaits approval)
                         │                              │
                         ▼                              ▼
              Debugging Agent ◀──── failures ─── (runs tests, hits bugs)
              (triages, ranks hypotheses)
```

---

## The 5 Reusable Skills

| # | Skill | What It Does | Used By |
|---|-------|-------------|---------|
| 1 | **semantic-search** | Find files by meaning, not keywords; returns ranked results | Documentation, Debugging, Refactoring, Feature |
| 2 | **citation-extract** | Extract exact quotes with `file:line` / `section` references | Requirements, Documentation, Debugging, Feature |
| 3 | **impact-graph** | Build caller/callee/test dependency graph for a symbol | Refactoring, Feature, Debugging |
| 4 | **pattern-match-failures** | Match a new failure against a library of known root causes | Debugging, Feature |
| 5 | **diff-summarize** | Produce reviewable diff summary with risk annotations | Refactoring, Requirements |

### Skill ↔ Agent Matrix

|               | semantic-search | citation-extract | impact-graph | pattern-match-failures | diff-summarize |
|---------------|:---:|:---:|:---:|:---:|:---:|
| Requirements  | ✅ | ✅ | — | — | ✅ |
| Documentation | ✅ | ✅ | — | — | — |
| Debugging     | ✅ | ✅ | ✅ | ✅ | — |
| Refactoring   | ✅ | — | ✅ | — | ✅ |
| Feature       | ✅ | ✅ | ✅ | ✅ | — |

---

## How the Design Satisfies "Reusable, Reviewable, Bounded"

| Requirement | How |
|-------------|-----|
| **Reusable** | 5 skills shared across 5 agents; no skill is agent-specific. The matrix above shows every skill serves ≥2 agents. |
| **Reviewable** | Every agent output includes citations (`file:line` or `section`) via `citation-extract`. The Refactoring Agent produces a reviewable diff via `diff-summarize` and blocks for human approval. |
| **Bounded** | Each agent has explicit DO NOT / ONLY constraints in its frontmatter body — it cannot drift into chatbot territory. |

---

## Getting Started

### For Teammates

1. **Clone** this repo
2. Open in VS Code with Copilot — agents and skills are auto-discovered from `.github/`
3. Invoke any agent via the chat agent picker (`@agent-name`) or let Copilot auto-delegate based on the `description` field
4. Invoke any skill via `/skill-name` in chat

### File Conventions

- **Agents** are in `.github/agents/*.agent.md` — each has YAML frontmatter (`description`, `tools`, `user-invocable`) and a body with Constraints, Approach, and Output Format
- **Skills** are in `.github/skills/<name>/SKILL.md` — each has YAML frontmatter (`name`, `description`, `argument-hint`) and a body with When to Use, Procedure, and Output Format
- **Failure library** (optional) lives in `.github/failures/` as markdown files consumed by the `pattern-match-failures` skill

---

## License

MIT
