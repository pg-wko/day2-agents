---
name: sphinx-config-manager
description: "Initialize, validate, and manage Sphinx documentation configuration (conf.py, index.rst, autodoc/napoleon extensions, themes, sys.path). Use when establishing or updating documentation build settings."
argument-hint: "Docs source path, Python package source path, and project metadata options"
---

# Sphinx Config Manager

## Purpose

Establish a robust, repeatable Sphinx documentation environment with required autodoc, napoleon, and viewcode extensions without manual configuration errors.

## Parameters & Inputs

- `docs_source_dir` (Path): Directory where Sphinx source configuration (`conf.py`, `index.rst`) is stored.
- `python_source_dir` (Path): Target Python package/source directory to resolve in `sys.path`.
- `project_name` (string): Human-readable name of the project.
- `author` (string): Authorship/organization string.
- `version` (string, optional): Documentation release version (default: `"1.0.0"`).
- `theme` (string, optional): HTML theme (default: `"sphinx_rtd_theme"` with fallback to `"alabaster"`).

## Procedure

1. Verify target `docs_source_dir` exists or create parent hierarchy.
2. Resolve the relative and absolute `sys.path` entries to target `python_source_dir`.
3. Configure core Sphinx extensions:
   - `sphinx.ext.autodoc`: Extracts docstrings from Python modules.
   - `sphinx.ext.napoleon`: Parses Google and NumPy style docstrings.
   - `sphinx.ext.viewcode`: Links generated documentation to source code.
   - `sphinx.ext.githubpages`: Generates `.nojekyll` for GitHub Pages hosting.
4. Generate `conf.py` with reproducible settings and theme configuration.
5. Generate `index.rst` table-of-contents root if missing.
6. Return a structured `SphinxSkillResult`.

## Output Format

```markdown
## Sphinx Config Record

**Docs Source Directory:** <path>
**Target Python Source:** <path>
**Status:** Success / Failed
**Configured Extensions:** sphinx.ext.autodoc, sphinx.ext.napoleon, sphinx.ext.viewcode, sphinx.ext.githubpages
**Theme:** <theme>
```

## Boundaries

- Do not hardcode machine-specific absolute paths into version-controlled configuration templates.
- Do not add undocumented third-party extensions not present in the workspace environment.
