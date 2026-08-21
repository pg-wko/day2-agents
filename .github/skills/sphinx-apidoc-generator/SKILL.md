---
name: sphinx-apidoc-generator
description: "Automatically inspect Python packages and generate reStructuredText (.rst) API source stubs using sphinx-apidoc. Use when creating or synchronizing Sphinx API references with source code."
argument-hint: "Python source directory and target documentation source directory"
---

# Sphinx APIDoc Generator

## Purpose

Automate the extraction of Python package and module structures into reStructuredText (`.rst`) stubs so Sphinx can generate comprehensive API reference pages via `autodoc`.

## Parameters & Inputs

- `python_source_dir` (Path): Path to the target Python code or package folder (e.g. `SamplePythonAPI/app`).
- `docs_source_dir` (Path): Output directory where generated `.rst` stubs will be placed (e.g. `SamplePythonAPI/docs/source`).
- `force_overwrite` (boolean, optional): Overwrite existing `.rst` files (`-f`, default: `true`).
- `separate_modules` (boolean, optional): Put documentation for each module on its own page (`-e`, default: `false`).

## Procedure

1. Verify existence of `python_source_dir` and scan for valid `.py` modules.
2. Formulate `sphinx.ext.apidoc` command with target flags (`-f`, `-o`).
3. Execute `sphinx-apidoc` subprocess within the active Python environment.
4. Verify created `.rst` files (e.g., `modules.rst`, `app.rst`).
5. Return execution summary and generated stub list.

## Output Format

```markdown
## APIDoc Generation Record

**Python Source Directory:** <path>
**Output RST Directory:** <path>
**Exit Code:** 0
**Generated RST Files:**
- `modules.rst`
- `<package>.rst`
```

## Boundaries

- Do not modify source Python files during `.rst` stub generation.
- Escalate errors if Python source code contains fatal syntax errors preventing AST inspection.
