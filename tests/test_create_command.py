"""
Integration tests for the 'create' command running from bin/modmaker entrypoint
"""

import os
import sys
import tempfile
import subprocess
import shutil
import pytest
from pathlib import Path


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for project creation tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_create_command_help(modmaker_bin_path):
    """Test the create command help works correctly"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "create", "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "create" in result.stdout


def test_create_project_help(modmaker_bin_path):
    """Test the create project command help works correctly"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "create", "project", "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    
    # Command should exit successfully
    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    
    # Help should contain usage information
    assert "usage:" in result.stdout
    assert "project" in result.stdout
    assert "name" in result.stdout


def test_create_with_invalid_arguments(modmaker_bin_path, temp_project_dir):
    """Test the create command with invalid arguments"""
    result = subprocess.run(
        [
            sys.executable,
            modmaker_bin_path,
            "create",
            "--type", "invalid_type",
            "--name", "test_project",
            "--output-dir", temp_project_dir
        ],
        capture_output=True,
        text=True,
        check=False
    )
    
    # Command should fail with non-zero exit code
    assert result.returncode != 0
    
    # Error message should mention the invalid type
    assert "invalid" in result.stderr.lower() and "type" in result.stderr.lower()


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])