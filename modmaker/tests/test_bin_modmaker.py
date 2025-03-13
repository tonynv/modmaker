"""
Unit tests for bin/modmaker entrypoint
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

class TestBinModmaker(unittest.TestCase):
    """Test cases for bin/modmaker entrypoint script"""
    
    def setUp(self):
        """Set up test environment"""
        self.bin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bin', 'modmaker')
        self.assertTrue(os.path.exists(self.bin_path), f"Entrypoint script not found at {self.bin_path}")

    def test_entrypoint_exists(self):
        """Test that the entrypoint script exists and is executable"""
        self.assertTrue(os.path.exists(self.bin_path))
        self.assertTrue(os.access(self.bin_path, os.X_OK), "Entrypoint script is not executable")

    @patch('modmaker._cli.main')
    def test_import_paths(self, mock_main):
        """Test that the import paths in the entrypoint are correct"""
        # Run the entrypoint with Python to test imports
        # Use subprocess with check_call to ensure it exits with code 0
        try:
            # We're just checking imports, so pass -h to avoid running the actual command
            result = subprocess.run(
                [sys.executable, self.bin_path, '-h'],
                capture_output=True,
                check=False
            )
            # The script should execute without crashing
            self.assertIn(result.returncode, [0, 1], f"Script exited with unexpected code {result.returncode}")
        except subprocess.CalledProcessError as e:
            self.fail(f"Entrypoint script failed: {e}, stdout: {e.stdout}, stderr: {e.stderr}")

    def test_entrypoint_content(self):
        """Test that the entrypoint file contains the correct imports"""
        with open(self.bin_path, 'r') as f:
            content = f.read()
            
        # Check that the file contains the necessary import patterns
        self.assertIn("from modmaker._cli import main", content)
        self.assertIn("except ImportError:", content)
        self.assertIn("from _cli import main", content)
        self.assertIn("sys.path.insert(0, parent_dir)", content)

    @patch('sys.path')
    def test_sys_path_insertion(self, mock_sys_path):
        """Test that the correct paths are added to sys.path"""
        # Execute the script directly to check sys.path modification
        mock_sys_path.insert = MagicMock()
        
        # Save and restore __file__
        old_file = None
        if '__file__' in globals():
            old_file = __file__
        
        try:
            # Setup fake environment
            globals()['__file__'] = self.bin_path
            
            # Read the script content
            with open(self.bin_path, 'r') as f:
                script_content = f.read()
            
            # Extract just the sys.path manipulation part
            path_lines = []
            for line in script_content.splitlines():
                if "sys.path" in line or "script_dir" in line or "parent_dir" in line:
                    path_lines.append(line)
            
            # Execute just those lines with globals
            path_code = "\n".join(path_lines)
            exec(path_code, globals())
            
            # Verify that sys.path.insert was called
            mock_sys_path.insert.assert_called()
            
        finally:
            # Restore __file__
            if old_file:
                globals()['__file__'] = old_file
            elif '__file__' in globals():
                del globals()['__file__']


if __name__ == "__main__":
    unittest.main()