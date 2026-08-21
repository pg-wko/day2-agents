# Task 1 — Documentation Workflow Diagram

## Deliverable

| File | Description |
|------|-------------|
| `docs/task1/documentation_workflow.png` | Visual workflow diagram (PNG, 200 DPI) |
| `scripts/generate_workflow_diagram.py` | Reproducible Python script that generates the diagram |
| `docs/task1/workflow_notes.md` | This file — explanatory notes |

---

## Workflow Overview

The diagram depicts a **five-phase, end-to-end documentation pipeline** for the
`SamplePythonAPI` ticketing system project. Each phase is a coloured box with a
phase number, title, subtitle, and key activities. The **Documentation Agent**
interacts with every phase — shown as dashed amber boxes above each phase with a
bidirectional dotted connector.

Sequential flow runs **left → right** (solid dark arrows). Feedback loops are
shown as **curved blue dashed arrows** beneath the main row, indicating where the
pipeline can re-cycle to an earlier phase.

---

## Phase Summary

### Phase 1 — Scope Identification
> **Goal:** Define *what* to document and *how deep*.

| Step | Description |
|------|-------------|
| 1.1 | Identify the target codebase / modules (e.g. `SamplePythonAPI/app/`) |
| 1.2 | Determine audience (developers, API consumers, new hires) and doc depth |
| 1.3 | Set success criteria and project boundaries |

**Agent action:** Receives the project path, scans file types (`.py`, `.rst`,
config files), and proposes a scope boundary document for human approval before
proceeding.

---

### Phase 2 — File / Logic Analysis
> **Goal:** Understand the code structure before writing any documentation.

| Step | Description |
|------|-------------|
| 2.1 | Parse the AST for each Python module (`main.py`, `api.py`, `models.py`, `database.py`, `ui.py`) |
| 2.2 | Map class and function dependencies (e.g. `TicketRepository` ↔ `Ticket`, `create_api_router` ↔ `TicketRepository`) |
| 2.3 | Identify public APIs, entry points (`create_app`, `create_api_router`), and data models (`Ticket`, `TicketCreate`, `TicketUpdate`) |

**Agent action:** Walks the codebase, builds a symbol dependency map, classifies
each module by role (API layer, data layer, UI layer, models), and produces a
structured summary that feeds into Phase 3.

---

### Phase 3 — Inline Documentation Application
> **Goal:** Generate or update docstrings, type annotations, and inline comments.

| Step | Description |
|------|-------------|
| 3.1 | Generate / update Google-style module and function docstrings |
| 3.2 | Verify and add type annotations where missing (e.g. return types, parameter types) |
| 3.3 | Insert contextual inline comments for complex logic (e.g. DuckDB connection lifecycle, thread lock usage) |

**Agent action:** Writes docstrings for every public symbol (classes, methods,
functions), inserts module-level docstrings, validates them with a parser, and
returns a diff for human review.

**→ Feedback to Phase 2:** If the agent discovers undocumented public symbols or
missing context during docstring generation, it loops back to Phase 2 to re-analyze
the relevant modules.

---

### Phase 4 — Sphinx Generation
> **Goal:** Build a complete, navigable documentation site from the annotated code.

| Step | Description |
|------|-------------|
| 4.1 | Configure Sphinx — create `conf.py`, `index.rst`, and extension list (`sphinx.ext.autodoc`, `sphinx.ext.napoleon`) |
| 4.2 | Run `sphinx-apidoc` to auto-generate RST source files from the codebase |
| 4.3 | Build HTML (and optionally PDF) output via `sphinx-build` |
| 4.4 | Collect build warnings and broken cross-references for review |

**Agent action:** Scaffolds the Sphinx project structure, invokes `sphinx-apidoc`
and `sphinx-build` commands programmatically, captures stdout/stderr, and
classifies any warnings for triage.

**→ Feedback to Phase 3:** If Sphinx reports missing docstrings, broken
references, or RST formatting errors, the agent loops back to Phase 3 to fix the
inline documentation and re-runs the build.

---

### Phase 5 — Review & Maintenance
> **Goal:** Verify accuracy and keep docs up to date over time.

| Step | Description |
|------|-------------|
| 5.1 | Human reviewer checks generated docs for accuracy, completeness, and tone |
| 5.2 | Fix any remaining warnings or broken references surfaced by the Sphinx build |
| 5.3 | Set up CI hooks (e.g. pre-commit, GitHub Actions) to re-run the pipeline when code changes |

**Agent action:** Surfaces a structured review document (diff of new/changed
docstrings, list of Sphinx warnings resolved/unresolved), and registers a CI task
that re-triggers the full pipeline on every push to the main branch.

**→ Feedback to Phase 1:** When code changes are merged, the CI hook sends the
agent back to Phase 1 to re-scope and re-run the entire documentation pipeline.

---

## Agent Interaction Points

The Documentation Agent is involved at **every phase**, but with different roles:

| Phase | Agent Role | Interaction Type |
|-------|-----------|-----------------|
| 1. Scope Identification | **Proposal** — suggests scope; waits for human approval | Bidirectional (propose ↔ approve) |
| 2. File / Logic Analysis | **Autonomous** — parses and classifies code | One-way (agent feeds Phase 3) |
| 3. Inline Documentation | **Generative** — writes docstrings, submits diffs for review | Bidirectional (generate ↔ review) |
| 4. Sphinx Generation | **Automation** — runs build commands, captures output | One-way (agent builds and reports) |
| 5. Review & Maintenance | **Monitoring** — registers CI hooks, surfaces diffs | Bidirectional (report ↔ re-trigger) |

In the diagram, **dashed amber boxes** above each phase represent the agent's
specific action, connected to the phase box by a **dotted amber bi-directional
arrow** (`<->`), indicating the agent both reads from and writes to that phase.

---

## Sequence & Dependencies

```text
Phase 1  ──▶  Phase 2  ──▶  Phase 3  ──▶  Phase 4  ──▶  Phase 5
Scope        Analysis      Inline       Sphinx       Review &
             (review)      docs         build        maintenance

           ▲                     ▲                     ▲
           │                     │                     │
           └──── re-analyze ────┴── fix docs ───────┴── CI re-run

Notes:
- Phase 1 → 2: scope defines the analysis target.
- Phase 2 → 3: docs are written from the code map.
- Phase 3 → 4: Sphinx needs fully annotated source.
- Phase 4 → 5: review validates the generated docs.
- Phase 3 → 2: missing context triggers re-analysis.
- Phase 4 → 3: warnings trigger doc updates.
- Phase 5 → 1: code changes restart the workflow.
```

- **Phase 1 → 2** (sequential): Analysis requires a defined scope.
- **Phase 2 → 3** (sequential): Docstring generation requires a symbol map.
- **Phase 3 → 4** (sequential): Sphinx build requires annotated code.
- **Phase 4 → 5** (sequential): Review requires built documentation output.
- **Phase 3 → 2** (feedback): Missing context triggers re-analysis.
- **Phase 4 → 3** (feedback): Sphinx warnings trigger docstring fixes.
- **Phase 5 → 1** (feedback): CI / code-changed re-triggers the full pipeline.

---

## Acceptance Criteria Checklist

| Criterion | Status | Where |
|-----------|--------|-------|
| All phases are represented | ✅ | Phases 1–5 are shown as coloured boxes |
| Arrows show the sequence and dependencies | ✅ | Solid arrows for sequential flow; dashed arrows for feedback loops |
| Diagram clearly indicates agent interaction points | ✅ | Dashed amber boxes above each phase with bi-directional connectors |
| Explanatory notes included | ✅ | This document |
