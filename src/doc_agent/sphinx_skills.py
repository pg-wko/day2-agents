"""Sphinx Automation Tool Wrappers and Skills for Documentation Agent.

Provides reusable capabilities for:
1. SphinxConfigManager: Initializing and validating Sphinx environment configurations.
2. SphinxApidocGenerator: Generating reStructuredText (.rst) API stubs from Python source.
3. SphinxDocBuilder: Compiling static HTML/PDF documentation with strict error/warning trapping.
4. SphinxDocstringAuditor: Auditing Python modules for autodoc/napoleon docstring compliance.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
import logging
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

logger = logging.getLogger("DocAgent.SphinxSkills")


@dataclass
class SphinxConfigOptions:
    project_name: str
    author: str
    version: str = "1.0.0"
    theme: str = "sphinx_rtd_theme"
    extensions: list[str] = field(
        default_factory=lambda: [
            "sphinx.ext.autodoc",
            "sphinx.ext.napoleon",
            "sphinx.ext.viewcode",
            "sphinx.ext.githubpages",
        ]
    )


@dataclass
class SphinxSkillResult:
    success: bool
    skill_name: str
    message: str
    output_path: Path | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class SphinxConfigManager:
    """Skill wrapper to initialize, validate, and manage Sphinx configuration files."""

    @staticmethod
    def setup_configuration(
        docs_source_dir: str | Path,
        python_source_dir: str | Path,
        options: SphinxConfigOptions,
    ) -> SphinxSkillResult:
        """Generates conf.py and index.rst in the documentation source directory.

        Args:
            docs_source_dir: Path to documentation source folder (where conf.py lives).
            python_source_dir: Path to the target Python source package/code directory.
            options: Configuration parameters for Sphinx.

        Returns:
            SphinxSkillResult containing status and generated file paths.
        """
        source_dir = Path(docs_source_dir).resolve()
        py_source_dir = Path(python_source_dir).resolve()
        source_dir.mkdir(parents=True, exist_ok=True)

        conf_file = source_dir / "conf.py"
        index_file = source_dir / "index.rst"

        try:
            # Generate conf.py
            extensions_repr = ",\n    ".join([f'"{ext}"' for ext in options.extensions])
            conf_code = f'''# Configuration file for the Sphinx documentation builder.
import os
import sys
from pathlib import Path

# Add python source directories to sys.path for autodoc resolution
sys.path.insert(0, str(Path(r"{py_source_dir.parent}").resolve()))
sys.path.insert(0, str(Path(r"{py_source_dir}").resolve()))

project = "{options.project_name}"
copyright = "2026, {options.author}"
author = "{options.author}"
release = "{options.version}"

extensions = [
    {extensions_repr}
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "{options.theme}" if "{options.theme}" in sys.modules or os.path.exists(r"{sys.prefix}") else "alabaster"
html_static_path = []
'''
            with open(conf_file, "w", encoding="utf-8") as f:
                f.write(conf_code)

            # Generate index.rst if missing
            if not index_file.exists():
                index_rst = f""".. {options.project_name} documentation master file

Welcome to {options.project_name}'s documentation!
==================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
                with open(index_file, "w", encoding="utf-8") as f:
                    f.write(index_rst)

            return SphinxSkillResult(
                success=True,
                skill_name="sphinx-config-manager",
                message=f"Configured Sphinx environment at {source_dir}",
                output_path=conf_file,
                metadata={"conf_file": str(conf_file), "index_file": str(index_file)},
            )
        except Exception as err:
            logger.error("SphinxConfigManager failed: %s", err, exc_info=True)
            return SphinxSkillResult(
                success=False,
                skill_name="sphinx-config-manager",
                message=str(err),
                errors=[str(err)],
            )


class SphinxApidocGenerator:
    """Skill wrapper to execute sphinx-apidoc and generate module .rst stubs."""

    @staticmethod
    def generate_api_stubs(
        python_source_dir: str | Path,
        docs_source_dir: str | Path,
        force_overwrite: bool = True,
        separate_modules: bool = False,
    ) -> SphinxSkillResult:
        """Runs sphinx.ext.apidoc to create .rst files for all modules in python_source_dir.

        Args:
            python_source_dir: Target Python package directory.
            docs_source_dir: Output folder for .rst files.
            force_overwrite: Whether to overwrite existing .rst stubs (-f).
            separate_modules: Put documentation for each module on its own page (-e).

        Returns:
            SphinxSkillResult with generated stub paths and apidoc logs.
        """
        py_source = Path(python_source_dir).resolve()
        docs_source = Path(docs_source_dir).resolve()
        docs_source.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            "-m",
            "sphinx.ext.apidoc",
            "-o",
            str(docs_source),
            str(py_source),
        ]
        if force_overwrite:
            cmd.append("-f")
        if separate_modules:
            cmd.append("-e")

        logger.info("Executing SphinxApidocGenerator: %s", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)

        rst_files = list(docs_source.glob("*.rst"))
        if result.returncode != 0:
            return SphinxSkillResult(
                success=False,
                skill_name="sphinx-apidoc-generator",
                message="sphinx-apidoc failed",
                errors=[result.stderr],
                metadata={"stdout": result.stdout, "stderr": result.stderr},
            )

        return SphinxSkillResult(
            success=True,
            skill_name="sphinx-apidoc-generator",
            message=f"Generated {len(rst_files)} .rst API stubs in {docs_source}",
            output_path=docs_source,
            metadata={
                "rst_files": [f.name for f in rst_files],
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )


class SphinxDocBuilder:
    """Skill wrapper to compile documentation into static HTML/PDF with strict validation."""

    @staticmethod
    def build_html(
        docs_source_dir: str | Path,
        docs_build_dir: str | Path,
        strict_warnings: bool = True,
        fresh_env: bool = False,
    ) -> SphinxSkillResult:
        """Builds static HTML documentation via sphinx-build.

        Args:
            docs_source_dir: Directory containing conf.py and .rst files.
            docs_build_dir: Target output directory for HTML files.
            strict_warnings: If True, treats warnings as errors (-W --keep-going).
            fresh_env: If True, do not use a saved environment, write all files (-E).

        Returns:
            SphinxSkillResult containing compilation metrics and status.
        """
        source_dir = Path(docs_source_dir).resolve()
        build_dir = Path(docs_build_dir).resolve()
        build_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "html",
            str(source_dir),
            str(build_dir),
        ]
        if strict_warnings:
            cmd.extend(["-W", "--keep-going"])
        if fresh_env:
            cmd.append("-E")

        logger.info("Executing SphinxDocBuilder: %s", " ".join(cmd))
        proc = subprocess.run(cmd, capture_output=True, text=True)

        index_html = build_dir / "index.html"
        warnings = [line for line in proc.stderr.splitlines() if "WARNING:" in line]
        errors = [line for line in proc.stderr.splitlines() if "ERROR:" in line]

        if proc.returncode != 0 or not index_html.exists():
            return SphinxSkillResult(
                success=False,
                skill_name="sphinx-doc-builder",
                message=f"Sphinx compilation failed with exit code {proc.returncode}",
                warnings=warnings,
                errors=errors or [proc.stderr],
                metadata={"stdout": proc.stdout, "stderr": proc.stderr},
            )

        return SphinxSkillResult(
            success=True,
            skill_name="sphinx-doc-builder",
            message=f"Sphinx HTML documentation built successfully at {build_dir}",
            output_path=index_html,
            warnings=warnings,
            metadata={
                "index_html": str(index_html),
                "stdout": proc.stdout,
                "warnings_count": len(warnings),
            },
        )


class SphinxDocstringAuditor:
    """Skill wrapper to verify docstring coverage and format before building documentation."""

    @staticmethod
    def audit_docstrings(package_dir: str | Path) -> SphinxSkillResult:
        """Parses Python AST across files to check for missing docstrings on classes and functions.

        Args:
            package_dir: Directory containing Python source files.

        Returns:
            SphinxSkillResult with coverage metrics and audit report.
        """
        pkg_path = Path(package_dir).resolve()
        py_files = sorted(list(pkg_path.glob("**/*.py")))

        total_nodes = 0
        documented_nodes = 0
        missing_docstrings: list[dict[str, Any]] = []

        for file_path in py_files:
            rel_path = file_path.relative_to(pkg_path)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=str(file_path))
            except SyntaxError as e:
                return SphinxSkillResult(
                    success=False,
                    skill_name="sphinx-docstring-auditor",
                    message=f"Syntax error in {rel_path}: {e}",
                    errors=[str(e)],
                )

            # Check module docstring
            total_nodes += 1
            if ast.get_docstring(tree):
                documented_nodes += 1
            else:
                missing_docstrings.append({"file": str(rel_path), "type": "module", "name": file_path.stem})

            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    total_nodes += 1
                    if ast.get_docstring(node):
                        documented_nodes += 1
                    else:
                        missing_docstrings.append({"file": str(rel_path), "type": "class", "name": node.name, "line": node.lineno})

                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if not item.name.startswith("_") or item.name == "__init__":
                                total_nodes += 1
                                if ast.get_docstring(item):
                                    documented_nodes += 1
                                else:
                                    missing_docstrings.append({"file": str(rel_path), "type": "method", "name": f"{node.name}.{item.name}", "line": item.lineno})
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not node.name.startswith("_"):
                        total_nodes += 1
                        if ast.get_docstring(node):
                            documented_nodes += 1
                        else:
                            missing_docstrings.append({"file": str(rel_path), "type": "function", "name": node.name, "line": node.lineno})

        coverage_pct = round((documented_nodes / total_nodes * 100), 2) if total_nodes > 0 else 100.0
        return SphinxSkillResult(
            success=True,
            skill_name="sphinx-docstring-auditor",
            message=f"Docstring coverage: {coverage_pct}% ({documented_nodes}/{total_nodes} items documented)",
            metadata={
                "total_items": total_nodes,
                "documented_items": documented_nodes,
                "coverage_percentage": coverage_pct,
                "missing_docstrings": missing_docstrings,
            },
        )
