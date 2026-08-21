"""Documentation Agent Pipeline Execution Script.

Runs the 5-phase automated documentation workflow against a target codebase.
"""

from pathlib import Path
import sys

# Add project root and src directory to python search path
REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from doc_agent.engine import DocumentationWorkflowEngine
except ImportError:
    from src.doc_agent.engine import DocumentationWorkflowEngine


def main() -> int:
    sample_api_dir = REPO_ROOT / "SamplePythonAPI"
    source_code_dir = sample_api_dir / "app"
    docs_output_dir = sample_api_dir / "docs"

    engine = DocumentationWorkflowEngine(
        project_root=sample_api_dir,
        source_dir=source_code_dir,
        docs_dir=docs_output_dir,
        project_name="Ticketing System API",
    )
    success = engine.run()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
