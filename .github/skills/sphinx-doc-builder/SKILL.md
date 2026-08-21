---
name: sphinx-doc-builder
description: "Compile Sphinx documentation into static HTML, PDF, or other targets with strict zero-warning validation (-W). Use when building, testing, or publishing engineering documentation."
argument-hint: "Docs source directory and target build directory"
---

# Sphinx Doc Builder

## Purpose

Build production-ready static documentation sites from Sphinx `.rst` sources and autodoc docstrings, enforcing strict zero-warning and zero-error standards.

## Parameters & Inputs

- `docs_source_dir` (Path): Directory containing `conf.py` and `.rst` sources.
- `docs_build_dir` (Path): Target directory for compiled HTML documentation (e.g. `docs/build/html`).
- `strict_warnings` (boolean, optional): If `true`, treats all Sphinx warnings as build-failing errors using `-W --keep-going` (default: `true`).
- `fresh_env` (boolean, optional): Force rebuild without cache using `-E` (default: `false`).

## Procedure

1. Verify `docs_source_dir` contains valid `conf.py` and `index.rst`.
2. Assemble `sphinx-build` execution arguments: builder target (`-b html`), strict flags (`-W`), source path, and output path.
3. Run the Sphinx compiler in the designated environment.
4. Scan compiler standard error and output logs for `WARNING:` or `ERROR:` lines.
5. Verify output artifacts (`index.html`, `genindex.html`, search indexes).
6. Return compilation metrics and result record.

## Output Format

```markdown
## Sphinx Build Record

**Docs Source Directory:** <path>
**Target Build Directory:** <path>
**Builder:** html
**Strict Warnings (-W):** Enabled
**Compilation Status:** Succeeded (0 Errors, 0 Warnings)
**Output Entrypoint:** `index.html`
```

## Boundaries

- Do not ignore Sphinx warnings when strict mode is requested.
- Do not publish artifacts when the build fails or produces broken cross-references.
