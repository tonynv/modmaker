"""
Integration tests for modmaker CLI through bin/modmaker entrypoint
"""

import os
import sys
import subprocess
import unittest
import pytest
from pathlib import Path


def test_modmaker_exists():
    """Verify the modmaker module exists."""
    import modmaker
    assert modmaker is not None


def test_help_command(modmaker_bin_path):
    """Test the help command runs successfully from the entrypoint"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    
    # Should exit with code 0 for help
    assert result.returncode == 0
    # Output should contain help text
    assert "usage:" in result.stdout
    assert "commands:" in result.stdout.lower()


def test_version_command(modmaker_bin_path):
    """Test the version command runs successfully from the entrypoint"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "--version"],
        capture_output=True,
        text=True,
        check=False
    )
    
    # Version should exit cleanly
    assert result.returncode == 0
    # Output should contain a version number
    assert result.stdout.strip()


def test_invalid_command(modmaker_bin_path):
    """Test the CLI handles invalid commands properly"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "nonexistentcommand"],
        capture_output=True,
        text=True,
        check=False
    )
    
    # Should exit with non-zero code for invalid command
    assert result.returncode != 0
    # Error message should be helpful
    assert "invalid choice" in result.stderr.lower() or "unknown command" in result.stderr.lower()


def test_debug_flag(modmaker_bin_path):
    """Test the debug flag works correctly"""
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "--debug", "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    
    assert result.returncode == 0
    # The help message should include mention of debug flag
    assert "--debug" in result.stdout
    assert "debug" in result.stdout.lower()


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])