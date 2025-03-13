"""
Tests for bin/modmaker entrypoint with focus on coverage
"""

import unittest
import pytest
import sys
import os
import subprocess
import importlib
from unittest.mock import patch, MagicMock
from pathlib import Path


def test_entrypoint_direct_import(modmaker_bin_path):
    """Test that the modmaker entrypoint can be executed directly"""
    # Get the directory containing the bin/modmaker script
    bin_dir = os.path.dirname(modmaker_bin_path)
    
    # We'll execute the script in a subprocess with PYTHONPATH set to ensure
    # the modmaker module can be imported directly
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(modmaker_bin_path).parents[1])
    
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "--version"],
        env=env,
        capture_output=True,
        text=True,
        check=False
    )
    
    # The script should execute successfully
    assert result.returncode == 0
    # Output should contain version information
    assert result.stdout.strip() != ""


def test_entrypoint_fallback_import(modmaker_bin_path):
    """Test the fallback import mechanism of the entrypoint"""
    # This test simulates what happens when the script can't find modmaker 
    # in the standard import paths and has to use sys.path manipulation
    
    # Execute with a clean environment and custom paths
    env = os.environ.copy()
    # Remove any paths that might contain modmaker from PYTHONPATH
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = ""
    
    result = subprocess.run(
        [sys.executable, modmaker_bin_path, "--help"],
        env=env,
        capture_output=True,
        text=True,
        check=False
    )
    
    # The script should execute successfully via fallback mechanisms
    assert result.returncode == 0
    assert "usage:" in result.stdout


def test_entrypoint_multi_import_attempts(modmaker_bin_path):
    """Test that multiple import attempts work in the entrypoint"""
    # This test creates a custom entrypoint script that forces all initial import attempts to fail
    # until the last one, simulating the fallback chain
    
    temp_script = """
import sys
import os
import importlib

# Mock the ImportError for the first attempts
class MockImportError(ImportError):
    pass

# Count import attempts
attempt_count = [0]

# Define our import function
def mock_import_main(*args, **kwargs):
    attempt_count[0] += 1
    
    # Only succeed on the third attempt
    if attempt_count[0] < 3:
        raise MockImportError("Simulated import error")
    
    # Return a mock main function on third attempt
    return lambda: print("Mock main function executed")

# Replace built-in import with our mock
original_import = __import__
def mock_import(name, *args, **kwargs):
    if name == 'modmaker._cli' or name == '_cli':
        raise MockImportError("Simulated import error")
    return original_import(name, *args, **kwargs)

# Patch sys.modules to make our import fail
sys.meta_path.insert(0, type('MockFinder', (), {
    'find_spec': lambda s, fullname, path, target: None if fullname in ['modmaker._cli', '_cli'] else None
})())

# Execute the entrypoint script
script_path = "{script_path}"
with open(script_path, 'r') as f:
    script_content = f.read()

# Replace the import statements with our mock
modified_script = script_content.replace('from modmaker._cli import main', 'main = mock_import_main()')

# Execute the modified script
try:
    exec(modified_script)
    print(f"Import attempts: {{attempt_count[0]}}")
except Exception as e:
    print(f"Script execution failed: {{e}}")
""".format(script_path=modmaker_bin_path)
    
    # Create a temporary script file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(temp_script)
        temp_script_path = temp_file.name
    
    try:
        # Execute the temp script
        result = subprocess.run(
            [sys.executable, temp_script_path],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Verify that the script executed successfully
        assert "Mock main function executed" in result.stdout
        assert "Import attempts: " in result.stdout
        
    finally:
        # Clean up the temporary file
        os.unlink(temp_script_path)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])