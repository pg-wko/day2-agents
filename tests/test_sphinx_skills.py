"""Unit and integration tests for Sphinx Skills."""

from pathlib import Path
import pytest
import sys

# Ensure src is on python path
REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from doc_agent.sphinx_skills import (
    SphinxApidocGenerator,
    SphinxConfigManager,
    SphinxConfigOptions,
    SphinxDocBuilder,
    SphinxDocstringAuditor,
)


@pytest.fixture
def test_dirs(tmp_path):
    sample_app = REPO_ROOT / "SamplePythonAPI" / "app"
    docs_source = tmp_path / "docs" / "source"
    docs_build = tmp_path / "docs" / "build" / "html"
    return {
        "app_dir": sample_app,
        "source_dir": docs_source,
        "build_dir": docs_build,
    }


def test_sphinx_docstring_auditor(test_dirs):
    """Test auditing docstrings across the sample application."""
    result = SphinxDocstringAuditor.audit_docstrings(test_dirs["app_dir"])
    assert result.success is True
    assert result.metadata["total_items"] > 0
    assert result.metadata["coverage_percentage"] >= 80.0


def test_sphinx_config_manager(test_dirs):
    """Test generating conf.py and index.rst with SphinxConfigManager."""
    options = SphinxConfigOptions(
        project_name="Test API",
        author="Unit Tester",
        version="2.0.0",
    )
    result = SphinxConfigManager.setup_configuration(
        docs_source_dir=test_dirs["source_dir"],
        python_source_dir=test_dirs["app_dir"],
        options=options,
    )
    assert result.success is True
    assert (test_dirs["source_dir"] / "conf.py").exists()
    assert (test_dirs["source_dir"] / "index.rst").exists()


def test_sphinx_apidoc_generator(test_dirs):
    """Test generating .rst stubs with SphinxApidocGenerator."""
    # First ensure conf is setup
    options = SphinxConfigOptions(project_name="Test API", author="Unit Tester")
    SphinxConfigManager.setup_configuration(
        docs_source_dir=test_dirs["source_dir"],
        python_source_dir=test_dirs["app_dir"],
        options=options,
    )

    result = SphinxApidocGenerator.generate_api_stubs(
        python_source_dir=test_dirs["app_dir"],
        docs_source_dir=test_dirs["source_dir"],
        force_overwrite=True,
    )
    assert result.success is True
    assert (test_dirs["source_dir"] / "modules.rst").exists()


def test_sphinx_doc_builder_zero_warnings(test_dirs):
    """Test compiling HTML with SphinxDocBuilder ensuring zero errors/warnings (-W)."""
    options = SphinxConfigOptions(project_name="Test API", author="Unit Tester")
    SphinxConfigManager.setup_configuration(
        docs_source_dir=test_dirs["source_dir"],
        python_source_dir=test_dirs["app_dir"],
        options=options,
    )
    SphinxApidocGenerator.generate_api_stubs(
        python_source_dir=test_dirs["app_dir"],
        docs_source_dir=test_dirs["source_dir"],
        force_overwrite=True,
    )

    build_result = SphinxDocBuilder.build_html(
        docs_source_dir=test_dirs["source_dir"],
        docs_build_dir=test_dirs["build_dir"],
        strict_warnings=True,
    )
    assert build_result.success is True
    assert len(build_result.warnings) == 0
    assert len(build_result.errors) == 0
    assert (test_dirs["build_dir"] / "index.html").exists()
    assert (test_dirs["build_dir"] / "modules.html").exists()
