import subprocess
import sys
from pathlib import Path


def test_sample_project_builds_documentation_without_warnings() -> None:
    project_root = Path(__file__).resolve().parent.parent / "SamplePythonAPI"
    docs_dir = project_root / "docs"
    output_dir = docs_dir / "_build" / "html"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "html",
            str(docs_dir),
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        cwd=project_root,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert "WARNING:" not in result.stdout
    assert output_dir.exists()
    assert (output_dir / "index.html").exists()
