# Configuration file for the Sphinx documentation builder.
import os
import sys
from pathlib import Path

# Add source directory to sys.path
sys.path.insert(0, str(Path(r"C:\Users\queenach\Downloads\PracticalAI\Day2\day2-agents\SamplePythonAPI").resolve()))
sys.path.insert(0, str(Path(r"C:\Users\queenach\Downloads\PracticalAI\Day2\day2-agents\SamplePythonAPI\app").resolve()))

project = "Ticketing System API"
copyright = "2026, Engineering Team"
author = "Engineering Team"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme" if "sphinx_rtd_theme" in sys.modules or os.path.exists(r"C:\Users\queenach\Downloads\PracticalAI\.venv") else "alabaster"
html_static_path = []
