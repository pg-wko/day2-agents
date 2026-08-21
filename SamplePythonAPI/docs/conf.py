from __future__ import annotations

import os
import sys

ROOT = os.path.abspath("..")
sys.path.insert(0, ROOT)

project = "SamplePythonAPI"
author = "SamplePythonAPI"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]
