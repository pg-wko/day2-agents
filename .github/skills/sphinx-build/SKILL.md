---
name: sphinx-build
description: "Build a configured Sphinx documentation project into HTML output and report warnings or failures. Use when the agent is ready to generate the documentation site."
argument-hint: "Project path and optional output directory"
---

# Sphinx Build

## Purpose

Generate the HTML documentation site from a configured Sphinx project and capture warnings or build errors.

## Procedure

1. Confirm the documentation directory exists and contains `conf.py`.
2. Invoke Sphinx in HTML mode against the project documentation tree.
3. If warnings or errors appear, capture them and route them back to the documentation-editing phase.
4. Return the output directory and the warnings summary.

## Input

- `project_path`: Python project root
- `docs_dir` (optional): Sphinx docs directory; defaults to `<project_path>/docs`
- `output_dir` (optional): build output directory; defaults to `<docs_dir>/_build/html`

## Expected Output

- A generated HTML site under the output directory
- Exit code 0 for successful builds
- A warning/error summary if the build failed or emitted warnings

## Example

```bash
python scripts/sphinx_build.py "C:/path/to/Project"
```

## Boundaries

- Do not hide warnings; treat them as actionable issues for the documentation pass.
- Do not claim success without a verified Sphinx exit code.
- Do not make code changes during the build step; use build output to trigger fixes in the documentation pass.
