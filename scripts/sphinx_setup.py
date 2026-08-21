from __future__ import annotations

from pathlib import Path


def create_sphinx_project(project_root: str | Path) -> Path:
    root = Path(project_root).resolve()
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "_static").mkdir(exist_ok=True)
    (docs_dir / "_templates").mkdir(exist_ok=True)

    package_root = root / "app"
    if not package_root.exists():
        raise FileNotFoundError(f"Package directory not found: {package_root}")

    conf_path = docs_dir / "conf.py"
    conf_path.write_text(
        '''from __future__ import annotations\n\nimport os\nimport sys\n\nROOT = os.path.abspath("..")\nsys.path.insert(0, ROOT)\n\nproject = "SamplePythonAPI"\nauthor = "SamplePythonAPI"\nrelease = "0.1.0"\n\nextensions = [\n    "sphinx.ext.autodoc",\n    "sphinx.ext.napoleon",\n    "sphinx.ext.viewcode",\n]\n\ntemplates_path = ["_templates"]\nexclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]\n\nhtml_theme = "sphinx_rtd_theme"\n\nhtml_static_path = ["_static"]\n''',
        encoding="utf-8",
    )

    index_path = docs_dir / "index.rst"
    index_path.write_text(
        """SamplePythonAPI Documentation\n==============================\n\n.. toctree::\n   :maxdepth: 2\n   :caption: Contents:\n\n   app\n\nWelcome to the SamplePythonAPI documentation site.\n""",
        encoding="utf-8",
    )

    app_page = docs_dir / "app.rst"
    app_page.write_text(
        """Application Package\n===================\n\n.. automodule:: app\n   :members:\n   :undoc-members:\n   :show-inheritance:\n\n.. automodule:: app.api\n   :members:\n   :undoc-members:\n   :show-inheritance:\n\n.. automodule:: app.database\n   :members:\n   :undoc-members:\n   :show-inheritance:\n\n.. automodule:: app.models\n   :members:\n   :undoc-members:\n   :show-inheritance:\n\n.. automodule:: app.ui\n   :members:\n   :undoc-members:\n   :show-inheritance:\n""",
        encoding="utf-8",
    )

    return docs_dir


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a minimal Sphinx documentation project for the sample Python app.")
    parser.add_argument("project_root", help="Root directory of the Python project to document")
    args = parser.parse_args()

    docs_dir = create_sphinx_project(args.project_root)
    print(f"Sphinx project created at {docs_dir}")
