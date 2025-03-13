"""
Pytest configuration for modmaker.

This file handles special configurations for testing the modmaker package,
including running all tests through the bin/modmaker entrypoint.
"""

import os
import sys
import pytest
from pathlib import Path


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


@pytest.fixture(scope="session")
def modmaker_bin_path():
    """Return the path to the bin/modmaker entrypoint."""
    # Find the project root from the test directory
    project_root = Path(__file__).parent.parent
    bin_path = project_root / "modmaker" / "bin" / "modmaker"
    
    if not bin_path.exists():
        pytest.fail(f"Entrypoint script not found at {bin_path}")
    
    # Ensure the script is executable
    if not os.access(bin_path, os.X_OK):
        pytest.fail(f"Entrypoint script at {bin_path} is not executable")
    
    return bin_path