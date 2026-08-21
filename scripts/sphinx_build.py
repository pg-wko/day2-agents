from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_docs(project_root: str | Path) -> Path:
    root = Path(project_root).resolve()
    docs_dir = root / "docs"
    if not docs_dir.exists():
        raise FileNotFoundError(f"Sphinx docs directory not found: {docs_dir}")

    output_dir = docs_dir / "_build" / "html"
    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        str(docs_dir),
        str(output_dir),
    ]

    subprocess.run(cmd, check=True, cwd=root)
    return output_dir


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build the Sphinx docs for a sample project.")
    parser.add_argument("project_root", help="Root directory of the Python project to document")
    args = parser.parse_args()

    output_dir = build_docs(args.project_root)
    print(f"Documentation build succeeded: {output_dir}")
