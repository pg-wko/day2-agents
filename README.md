# Build Your AI Engineering Team

## Scenario

Engineering teams investigate failures using test results, logs, error messages, source code, configuration, historical failures, test cases, validation results, and engineering documentation. This repository defines small, reviewable AI building blocks that can support those investigations.

The design is intentionally bounded: it specifies **five specialist agents** and **five reusable skills**. It does not attempt to design a complete AI platform or a generic chatbot.

## Design Principles

- **Reusable:** agents use shared skills with stable inputs and outputs.
- **Reviewable:** every conclusion includes evidence, assumptions, and a confidence level.
- **Bounded:** each agent has one engineering responsibility and must escalate work outside that boundary.
- **Human-approved:** agents may investigate and propose changes, but engineers review findings and approve any code or configuration changes.

## Specialist Agents

### 1. Feature Agent

**Responsibility:** turn an approved, scoped feature request into an implementation-ready engineering plan.

**Inputs:** requirements, relevant source code, API contracts, test cases, and engineering documentation.

**Outputs:** affected components, acceptance criteria, implementation steps, test plan, assumptions, and unresolved questions.

**Boundaries:** does not implement code, approve requirements, or make architecture decisions beyond the requested feature.

### 2. Debugging Agent

**Responsibility:** investigate a reported failure and produce evidence-backed root-cause hypotheses.

**Inputs:** logs, error messages, failing test results, configuration, recent changes, and historical failures.

**Outputs:** failure timeline, ranked hypotheses, supporting and contradicting evidence, reproduction steps, and recommended next diagnostic action.

**Boundaries:** does not silently change production configuration or claim a root cause without traceable evidence.

### 3. Documentation Agent

**Responsibility:** keep engineering documentation accurate after approved changes or investigations.

**Inputs:** approved implementation details, API changes, validation results, existing documentation, and review feedback.

**Outputs:** proposed documentation patch, affected audience, source references, and a checklist of claims that need technical review.

**Boundaries:** does not invent product behavior or publish documentation without a human reviewer confirming technical accuracy.

### 4. Refactoring Agent

**Responsibility:** identify and propose behavior-preserving improvements to code structure.

**Inputs:** source code, tests, static-analysis findings, code conventions, and coverage or validation results.

**Outputs:** refactoring proposal, expected invariants, risk assessment, incremental change plan, and regression-test plan.

**Boundaries:** does not combine refactoring with new features, change public behavior, or proceed when behavior is not sufficiently covered by tests.

### 5. Requirements Agent

**Responsibility:** make a technical requirement precise, testable, and internally consistent before implementation begins.

**Inputs:** feature request, stakeholder notes, existing behavior, constraints, documentation, and related historical failures.

**Outputs:** clarified requirement, acceptance criteria, non-functional constraints, ambiguity list, edge cases, and questions requiring a decision.

**Boundaries:** does not decide unresolved business priorities or reinterpret policy; it records choices for the responsible stakeholder.

## Reusable Skills

Each skill is a small capability shared by multiple agents. It returns structured evidence rather than an unqualified answer.

### 1. Evidence Extractor

Extracts relevant facts from logs, test output, source files, configuration, and documentation.

- **Input:** sources plus an investigation question.
- **Output:** evidence items with source location, timestamp or version when available, and relevance rationale.
- **Used by:** all five agents.

### 2. Change Impact Analyzer

Finds likely affected code, tests, configuration, interfaces, and documentation for a proposed change or observed failure.

- **Input:** change description or failure signature and repository context.
- **Output:** impacted artifacts, dependency path, confidence, and items requiring manual inspection.
- **Used by:** Feature, Debugging, Documentation, and Refactoring Agents.

### 3. Test and Validation Planner

Creates a proportional plan to verify a feature, fix, refactor, or documentation claim.

- **Input:** intended behavior, risks, existing tests, and validation constraints.
- **Output:** test cases, expected results, test data needs, and success criteria.
- **Used by:** Feature, Debugging, Refactoring, and Requirements Agents.

### 4. Historical Failure Matcher

Compares a current failure signature with prior incidents, fixes, postmortems, and known limitations.

- **Input:** error messages, stack traces, log patterns, and historical records.
- **Output:** ranked similar incidents, matching evidence, differences, and links to prior remediation.
- **Used by:** Debugging and Requirements Agents.

### 5. Review Packager

Packages an agent's work into a human-reviewable artifact.

- **Input:** findings, evidence, assumptions, proposed actions, and validation results.
- **Output:** summary, decision needed, risks, confidence, traceable references, and explicit out-of-scope items.
- **Used by:** all five agents.

## Review Workflow

1. An engineer selects the specialist agent that matches the work item.
2. The agent invokes only the skills needed for its bounded responsibility.
3. The agent produces a review package with evidence and open questions.
4. A human engineer reviews conclusions and approves any follow-up change.

## Repository Collaboration

This repository is intended to be public so teammates can review agent boundaries, skill contracts, and proposed refinements through issues and pull requests. Keep future contributions focused on a specific agent or reusable skill, with examples and validation criteria for any changed behavior.
