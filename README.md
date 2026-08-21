# Build Your AI Engineering Team

## Scenario

Engineering teams investigate failures using test results, logs, error messages, source code, configuration, historical failures, test cases, validation results, and engineering documentation. This repository defines small, reviewable AI building blocks that can support those investigations.

The design is intentionally bounded: it specifies **five specialist agents** and **five reusable skills**. It does not attempt to design a complete AI platform or a generic chatbot.

## Design Principles

- **Reusable:** agents use shared skills with stable inputs and outputs.
- **Reviewable:** every conclusion includes evidence, assumptions, and a confidence level.
- **Bounded:** each agent has one engineering responsibility and must escalate work outside that boundary.
- **Human-approved:** agents may investigate and propose changes, but engineers review findings and approve any code or configuration changes.

## Repository Structure

```text
.github/
	agents/                  # One focused .agent.md definition per engineering role
	skills/                  # One self-contained SKILL.md contract per reusable capability
docs/
	workflow/                # Workflow diagrams (.svg, .html)
	integration/             # Agent integration and architecture specifications
scripts/                     # Runnable developer automation scripts
	run_doc_pipeline.py      # Script to execute the documentation workflow
src/
	doc_agent/               # Modular agent pipelines and state machine engines
tests/                       # Automated test suites for agent engines
SamplePythonAPI/             # Target service codebase for demonstration
README.md                    # Team-facing catalogue and workflow
CONTRIBUTING.md              # Rules for adding or changing agents and skills
```

This layout scales by allowing agents to compose existing skills instead of duplicating investigation logic. A new capability belongs in a skill when multiple agents can reuse it; it belongs in an agent only when it defines a distinct engineering responsibility.

## Extension Contract

All additions must preserve these contracts:

- **Skills:** use `.github/skills/<lowercase-hyphenated-name>/SKILL.md`; include a discovery-focused `description`, purpose, procedure, structured output, and boundaries.
- **Agents:** use `.github/agents/<role>.agent.md`; include a focused `description`, minimal tool permissions, required skill links, procedure, boundaries, and reviewable output.
- **Inputs and outputs:** keep formats stable where other agents depend on them. Make incompatible output changes explicit and update every consuming agent in the same pull request.
- **Evidence:** identify sources by file path, test name, log timestamp, incident ID, or URL so reviewers can reproduce conclusions.
- **Safety:** skills and agents may propose work, but cannot silently approve requirements, publish documentation, or apply production changes.
- **Scope:** prefer a new specialist agent over expanding an existing agent beyond one engineering responsibility.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the review checklist and contribution workflow.

## Specialist Agents

### 1. [Feature Agent](.github/agents/feature.agent.md)

**Responsibility:** turn an approved, scoped feature request into an implementation-ready engineering plan.

**Inputs:** requirements, relevant source code, API contracts, test cases, and engineering documentation.

**Outputs:** affected components, acceptance criteria, implementation steps, test plan, assumptions, and unresolved questions.

**Boundaries:** does not implement code, approve requirements, or make architecture decisions beyond the requested feature.

### 2. [Debugging Agent](.github/agents/debugging.agent.md)

**Responsibility:** investigate a reported failure and produce evidence-backed root-cause hypotheses.

**Inputs:** logs, error messages, failing test results, configuration, recent changes, and historical failures.

**Outputs:** failure timeline, ranked hypotheses, supporting and contradicting evidence, reproduction steps, and recommended next diagnostic action.

**Boundaries:** does not silently change production configuration or claim a root cause without traceable evidence.

### 3. [Documentation Agent](.github/agents/documentation.agent.md)

**Responsibility:** keep engineering documentation accurate after approved changes or investigations.

**Inputs:** approved implementation details, API changes, validation results, existing documentation, and review feedback.

**Outputs:** proposed documentation patch, affected audience, source references, and a checklist of claims that need technical review.

**Boundaries:** does not invent product behavior or publish documentation without a human reviewer confirming technical accuracy.

### 4. [Refactoring Agent](.github/agents/refactoring.agent.md)

**Responsibility:** identify and propose behavior-preserving improvements to code structure.

**Inputs:** source code, tests, static-analysis findings, code conventions, and coverage or validation results.

**Outputs:** refactoring proposal, expected invariants, risk assessment, incremental change plan, and regression-test plan.

**Boundaries:** does not combine refactoring with new features, change public behavior, or proceed when behavior is not sufficiently covered by tests.

### 5. [Requirements Agent](.github/agents/requirements.agent.md)

**Responsibility:** make a technical requirement precise, testable, and internally consistent before implementation begins.

**Inputs:** feature request, stakeholder notes, existing behavior, constraints, documentation, and related historical failures.

**Outputs:** clarified requirement, acceptance criteria, non-functional constraints, ambiguity list, edge cases, and questions requiring a decision.

**Boundaries:** does not decide unresolved business priorities or reinterpret policy; it records choices for the responsible stakeholder.

## Reusable Skills

Each skill is a small capability shared by multiple agents. It returns structured evidence rather than an unqualified answer. Agent definitions declare the skills they consume; this catalogue describes when each skill is appropriate.

### 1. [Evidence Extractor](.github/skills/evidence-extractor/SKILL.md)

Extracts relevant facts from logs, test output, source files, configuration, and documentation.

- **Input:** sources plus an investigation question.
- **Output:** evidence items with source location, timestamp or version when available, and relevance rationale.
- **Intended use:** any agent that needs traceable facts from engineering sources.

### 2. [Change Impact Analyzer](.github/skills/change-impact-analyzer/SKILL.md)

Finds likely affected code, tests, configuration, interfaces, and documentation for a proposed change or observed failure.

- **Input:** change description or failure signature and repository context.
- **Output:** impacted artifacts, dependency path, confidence, and items requiring manual inspection.
- **Intended use:** agents evaluating the effect of a change or failure across engineering artifacts.

### 3. [Test and Validation Planner](.github/skills/test-validation-planner/SKILL.md)

Creates a proportional plan to verify a feature, fix, refactor, or documentation claim.

- **Input:** intended behavior, risks, existing tests, and validation constraints.
- **Output:** test cases, expected results, test data needs, and success criteria.
- **Intended use:** agents that need a proportionate, reviewable plan to verify behavior or claims.

### 4. [Historical Failure Matcher](.github/skills/historical-failure-matcher/SKILL.md)

Compares a current failure signature with prior incidents, fixes, postmortems, and known limitations.

- **Input:** error messages, stack traces, log patterns, and historical records.
- **Output:** ranked similar incidents, matching evidence, differences, and links to prior remediation.
- **Intended use:** agents comparing a current failure or risk against prior incidents and remediations.

### 5. [Review Packager](.github/skills/review-packager/SKILL.md)

Packages an agent's work into a human-reviewable artifact.

- **Input:** findings, evidence, assumptions, proposed actions, and validation results.
- **Output:** summary, decision needed, risks, confidence, traceable references, and explicit out-of-scope items.
- **Intended use:** any agent handing findings to a human engineer for review or decision.

### 6. [Sphinx Config Manager](.github/skills/sphinx-config-manager/SKILL.md)

Configures and initializes reproducible Sphinx environments (`conf.py`, `index.rst`, extensions, and themes).

- **Input:** documentation source directory, Python package directory, and project metadata.
- **Output:** status result with validated `conf.py` and `index.rst` paths.
- **Intended use:** documentation agents setting up Sphinx documentation workspaces.

### 7. [Sphinx APIDoc Generator](.github/skills/sphinx-apidoc-generator/SKILL.md)

Extracts Python module ASTs into reStructuredText (`.rst`) API stubs using `sphinx-apidoc`.

- **Input:** Python source code directory and target documentation source directory.
- **Output:** collection of generated `.rst` API definition files.
- **Intended use:** documentation agents creating or synchronizing API reference stubs.

### 8. [Sphinx Doc Builder](.github/skills/sphinx-doc-builder/SKILL.md)

Compiles Sphinx `.rst` sources and autodoc docstrings into static HTML sites with strict zero-warning verification (`-W`).

- **Input:** documentation source and output build directories.
- **Output:** compiled static HTML site, search index, and zero-warning build validation record.
- **Intended use:** agents and CI pipelines compiling and verifying documentation artifacts.

## Review Workflow

1. An engineer selects the specialist agent that matches the work item.
2. The agent invokes only the skills needed for its bounded responsibility.
3. The agent produces a review package with evidence and open questions.
4. A human engineer reviews conclusions and approves any follow-up change.

## Repository Collaboration

This repository is intended to be public so teammates can review agent boundaries, skill contracts, and proposed refinements through issues and pull requests. Keep future contributions focused on a specific agent or reusable skill, with examples and validation criteria for any changed behavior. Follow the contribution workflow in [CONTRIBUTING.md](CONTRIBUTING.md).
