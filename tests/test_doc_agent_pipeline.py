"""Tests for the Documentation Agent Automated Workflow Pipeline."""

import ast
from pathlib import Path
import pytest
import sys

# Ensure src is on Python search path
PACKAGE_DIR = Path(__file__).parent.parent
SRC_DIR = PACKAGE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from doc_agent.engine import DocumentationWorkflowEngine, WorkflowState


@pytest.fixture
def workflow_engine():
    current_dir = Path(__file__).parent.parent
    sample_api_dir = current_dir / "SamplePythonAPI"
    source_code_dir = sample_api_dir / "app"
    docs_output_dir = sample_api_dir / "docs"

    return DocumentationWorkflowEngine(
        project_root=sample_api_dir,
        source_dir=source_code_dir,
        docs_dir=docs_output_dir,
        project_name="Ticketing System API",
    )


def test_full_workflow_execution(workflow_engine):
    """Test that running the full workflow traverses all states and completes."""
    success = workflow_engine.run()
    assert success is True
    assert workflow_engine.state == WorkflowState.REVIEW_PACKAGED
    assert workflow_engine.docs_dir.exists()
    assert (workflow_engine.docs_dir / "build" / "html" / "index.html").exists()
    assert (workflow_engine.docs_dir / "ENGINEERING_REVIEW_PACKAGE.md").exists()


def test_phase_1_scope_identification(workflow_engine):
    """Test that Phase 1 properly maps files and target audience."""
    manifest = workflow_engine.phase_1_scope_identification()
    assert workflow_engine.state == WorkflowState.SCOPE_IDENTIFIED
    assert manifest["total_files"] >= 4
    assert "target_audience" in manifest


def test_phase_2_file_logic_analysis(workflow_engine):
    """Test that Phase 2 accurately extracts AST data without errors."""
    workflow_engine.phase_1_scope_identification()
    report = workflow_engine.phase_2_file_logic_analysis()
    assert workflow_engine.state == WorkflowState.LOGIC_ANALYZED
    assert report["total_analyzed_files"] >= 4


def test_phase_3_inline_docstrings(workflow_engine):
    """Test that Phase 3 ensures docstrings are applied."""
    workflow_engine.phase_1_scope_identification()
    workflow_engine.phase_2_file_logic_analysis()
    applied = workflow_engine.phase_3_inline_documentation()
    assert workflow_engine.state == WorkflowState.INLINE_DOCS_APPLIED
    assert applied >= 0

    # Verify models.py has docstring
    models_file = workflow_engine.source_dir / "models.py"
    with open(models_file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    assert ast.get_docstring(tree) is not None


def test_phase_4_and_5_sphinx_and_package(workflow_engine):
    """Test that Phase 4 builds Sphinx HTML and Phase 5 outputs review package."""
    workflow_engine.phase_1_scope_identification()
    workflow_engine.phase_2_file_logic_analysis()
    workflow_engine.phase_3_inline_documentation()
    html_dir = workflow_engine.phase_4_sphinx_generation()
    assert workflow_engine.state == WorkflowState.SPHINX_GENERATED
    assert (html_dir / "index.html").exists()

    pkg_path = workflow_engine.phase_5_review_and_packaging()
    assert workflow_engine.state == WorkflowState.REVIEW_PACKAGED
    assert pkg_path.exists()
