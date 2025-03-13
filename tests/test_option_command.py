"""
Integration tests for the 'option' command running from bin/modmaker entrypoint
"""

import os
import sys
import tempfile
import subprocess
import shutil
import pytest
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for option command tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_option_command_help(modmaker_bin_path):
    """Test the option command help works correctly"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "option", "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "option" in result.stdout


def test_option_help(modmaker_bin_path):
    """Test the option help command works correctly"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "option", "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    
    assert result.returncode == 0
    # Should show help for option command
    assert "option" in result.stdout.lower()


def test_option_with_invalid_subcommand(modmaker_bin_path):
    """Test the option command with invalid subcommand"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "option", "invalid_subcommand"],
        capture_output=True,
        text=True,
        check=False
    )
    
    # Command should fail with non-zero exit code
    assert result.returncode != 0
    
    # Error message should mention the invalid subcommand
    assert "invalid" in result.stderr.lower() or "unknown" in result.stderr.lower()


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])