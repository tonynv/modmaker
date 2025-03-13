"""
Pytest configuration for modmaker.

This file handles the special case of template files that contain
template variables that shouldn't be directly executed.
"""

import os
import sys
import pytest
from pathlib import Path

# Add the parent directory to sys.path to allow imports from the modmaker package
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def pytest_ignore_collect(collection_path, config):
    """Ignore test files in template directories that contain template variables."""
    # Check if the file is in a templates directory
    if "templates" in str(collection_path):
        # Only ignore test files (not conftest.py or __init__.py)
        if "test_" in str(collection_path):
            # Check for template variables in the file content
            try:
                with open(collection_path, "r") as f:
                    content = f.read()
                    if "{{PROJECT_NAME}}" in content and not "def test_template_exists" in content:
                        return True  # Ignore this file
            except Exception:
                pass
    return False