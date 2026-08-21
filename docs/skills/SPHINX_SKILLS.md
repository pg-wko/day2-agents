# Sphinx Automation Skills Documentation

This document describes the reusable Sphinx skills available to the **Documentation Agent** and CI/CD automation pipelines.

---

## 1. Skill Catalog

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Sphinx Skills Suite                              │
├─────────────────────────┬───────────────────────────────────────────────────┤
│ sphinx-config-manager   │ Sets up conf.py, index.rst, extensions, and theme │
├─────────────────────────┼───────────────────────────────────────────────────┤
│ sphinx-apidoc-generator │ Generates .rst stubs from Python packages         │
├─────────────────────────┼───────────────────────────────────────────────────┤
│ sphinx-doc-builder      │ Compiles HTML with zero-warning (-W) verification │
├─────────────────────────┼───────────────────────────────────────────────────┤
│ sphinx-docstring-auditor│ Audits Python AST for docstring completeness      │
└─────────────────────────┴───────────────────────────────────────────────────┘
```

---

## 2. Skill Specifications & Examples

### 1. `sphinx-config-manager`
* **Purpose:** Sets up and validates the Sphinx documentation workspace without manual boilerplate.
* **Module:** `src.doc_agent.sphinx_skills.SphinxConfigManager`
* **Parameters:**
  - `docs_source_dir` (`Path`): Directory where Sphinx source configuration lives.
  - `python_source_dir` (`Path`): Target Python code folder for `sys.path` resolution.
  - `options` (`SphinxConfigOptions`): Metadata including `project_name`, `author`, `version`, `theme`, and `extensions`.
* **Python Example:**
  ```python
  from doc_agent.sphinx_skills import SphinxConfigManager, SphinxConfigOptions

  opts = SphinxConfigOptions(
      project_name="Ticketing API",
      author="Engineering Team",
      version="1.0.0"
  )
  result = SphinxConfigManager.setup_configuration(
      docs_source_dir="SamplePythonAPI/docs/source",
      python_source_dir="SamplePythonAPI/app",
      options=opts
  )
  assert result.success is True
  ```

---

### 2. `sphinx-apidoc-generator`
* **Purpose:** Uses `sphinx-apidoc` to inspect Python code and generate `.rst` stubs.
* **Module:** `src.doc_agent.sphinx_skills.SphinxApidocGenerator`
* **Parameters:**
  - `python_source_dir` (`Path`): Source directory of Python modules.
  - `docs_source_dir` (`Path`): Output directory for `.rst` files.
  - `force_overwrite` (`bool`, default=`True`): Overwrite existing `.rst` files.
  - `separate_modules` (`bool`, default=`False`): Generate separate page per module.
* **Python Example:**
  ```python
  from doc_agent.sphinx_skills import SphinxApidocGenerator

  result = SphinxApidocGenerator.generate_api_stubs(
      python_source_dir="SamplePythonAPI/app",
      docs_source_dir="SamplePythonAPI/docs/source",
      force_overwrite=True
  )
  print(f"Generated RST files: {result.metadata['rst_files']}")
  ```

---

### 3. `sphinx-doc-builder`
* **Purpose:** Compiles Sphinx documentation to HTML with strict zero-warning validation (`-W`).
* **Module:** `src.doc_agent.sphinx_skills.SphinxDocBuilder`
* **Parameters:**
  - `docs_source_dir` (`Path`): Directory containing `conf.py` and `.rst` sources.
  - `docs_build_dir` (`Path`): Target output directory for HTML files.
  - `strict_warnings` (`bool`, default=`True`): Treat warnings as build-failing errors.
  - `fresh_env` (`bool`, default=`False`): Force re-reading all source files.
* **Python Example:**
  ```python
  from doc_agent.sphinx_skills import SphinxDocBuilder

  result = SphinxDocBuilder.build_html(
      docs_source_dir="SamplePythonAPI/docs/source",
      docs_build_dir="SamplePythonAPI/docs/build/html",
      strict_warnings=True
  )
  assert result.success is True
  print(f"Index generated at: {result.output_path}")
  ```

---

### 4. `sphinx-docstring-auditor`
* **Purpose:** Audits AST docstrings before invoking Sphinx compilation.
* **Module:** `src.doc_agent.sphinx_skills.SphinxDocstringAuditor`
* **Parameters:**
  - `package_dir` (`Path`): Directory containing Python source files.
* **Python Example:**
  ```python
  from doc_agent.sphinx_skills import SphinxDocstringAuditor

  audit = SphinxDocstringAuditor.audit_docstrings("SamplePythonAPI/app")
  print(f"Docstring coverage: {audit.metadata['coverage_percentage']}%")
  ```

---

## 3. Execution & Verification

Run the automated test suite for all Sphinx skills:

```powershell
pytest Day2/day2-agents/tests -v
```
