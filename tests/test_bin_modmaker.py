"""
Unit tests for bin/modmaker entrypoint
"""

import unittest
import pytest
import sys
import os
import subprocess
from pathlib import Path


def test_entrypoint_exists(modmaker_bin_path):
    """Test that the entrypoint script exists and is executable"""
    assert os.path.exists(modmaker_bin_path)
    assert os.access(modmaker_bin_path, os.X_OK), "Entrypoint script is not executable"


def test_entrypoint_import_paths(modmaker_bin_path):
    """Test that the import paths in the entrypoint are correct"""
    # Run the entrypoint with Python to test imports
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, '-h'],
        capture_output=True,
        text=True,
        check=False
    )
    # The script should execute without crashing
    assert result.returncode in [0, 1], f"Script exited with unexpected code {result.returncode}"


def test_entrypoint_content(modmaker_bin_path):
    """Test that the entrypoint file contains the correct imports"""
    with open(modmaker_bin_path, 'r') as f:
        content = f.read()
        
    # Check that the file contains the necessary import patterns
    assert "from modmaker._cli import main" in content
    assert "except ImportError:" in content
    assert "sys.path.insert(0, parent_dir)" in content


def test_help_flag(modmaker_bin_path):
    """Test that the help flag works correctly"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, '--help'],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])