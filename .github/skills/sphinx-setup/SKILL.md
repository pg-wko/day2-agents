---
name: sphinx-setup
description: "Create or refresh a Sphinx documentation project for a Python codebase, including configuration, package discovery, and the initial landing page. Use when an agent needs to scaffold docs before a documentation build."
argument-hint: "Project path to document and optional output directory"
---

# Sphinx Setup

## Purpose

Create a minimal, working Sphinx project for a Python package so the agent can generate API docs and a documentation landing page.

## Procedure

1. Confirm the target Python project path.
2. Create or update the documentation directory under the project root.
3. Configure Python import paths so autodoc can locate the package.
4. Enable core Sphinx extensions such as autodoc, napoleon, and viewcode.
5. Write a landing page that includes the package module hierarchy.
6. Return the configuration and output file paths.

## Input

- `project_path`: root directory of the Python project to document
- `docs_dir` (optional): documentation directory; defaults to `<project_path>/docs`

## Expected Output

- A generated `conf.py` file
- A generated `index.rst` landing page
- An API or modules page that includes the package modules
- A success message indicating where the documentation project was created

## Example

```bash
python scripts/sphinx_setup.py "C:/path/to/Project"
```

## Boundaries

- Do not modify business logic.
- Do not build the documentation site in this step; only scaffold the project.
- Do not claim package import success unless the configured import path matches the project layout.
