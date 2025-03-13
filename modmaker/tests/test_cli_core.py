"""
Unit tests for _cli_core.py
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import inspect
import argparse

# Import module under test
from modmaker._cli_core import CliCore


# Test fixtures
class TestCommand:
    """Test command class for CLI testing"""
    
    def __init__(self):
        """Initialize test command"""
        pass
    
    def command_with_doc(self, param1, param2=None):
        """
        Test command with docstring
        
        Args:
            param1: First parameter
            param2: Second parameter (optional)
        
        Returns:
            bool: Success status
        """
        return True
    
    def command_without_doc(self, param1):
        return True


class TestCliCore(unittest.TestCase):
    """Test cases for CliCore class"""

    def setUp(self):
        """Set up test fixtures"""
        self.name = "test_cli"
        self.version = "1.0.0"
        self.description = "Test CLI"
        self.global_args = [
            [
                ["-v", "--verbose"],
                {
                    "action": "store_true",
                    "help": "enable verbose output",
                    "dest": "_verbose",
                }
            ]
        ]
        
        # Create mock modules
        self.mock_module = MagicMock()
        self.mock_module.__name__ = "test_module"
        self.mock_module.TestCommand = TestCommand
        
        # Create CLI core instance
        self.cli = CliCore(
            self.name,
            {"test_module": self.mock_module},
            self.description,
            self.version,
            self.global_args
        )

    def test_init(self):
        """Test initialization"""
        self.assertEqual(self.cli.name, "test_cli")
        self.assertEqual(self.cli.version, "1.0.0")
        self.assertEqual(self.cli.description, "Test CLI")
        self.assertIsInstance(self.cli.parser, argparse.ArgumentParser)
        self.assertIsInstance(self.cli.subparsers, argparse._SubParsersAction)

    def test_get_class_methods(self):
        """Test _get_class_methods method"""
        command_class = TestCommand
        methods = self.cli._get_class_methods(command_class)
        
        # Should find our two test methods
        self.assertEqual(len(methods), 2)
        method_names = [m[0] for m in methods]
        self.assertIn("command_with_doc", method_names)
        self.assertIn("command_without_doc", method_names)
        
        # Should not include __init__
        self.assertNotIn("__init__", method_names)

    def test_get_param_help(self):
        """Test _get_param_help method"""
        command_class = TestCommand
        method = command_class.command_with_doc
        signature = inspect.signature(method)
        param = signature.parameters["param1"]
        
        help_text = self.cli._get_param_help(method.__doc__, param)
        self.assertEqual(help_text, "First parameter")
        
        # Test with optional parameter
        param2 = signature.parameters["param2"]
        help_text = self.cli._get_param_help(method.__doc__, param2)
        self.assertEqual(help_text, "Second parameter (optional)")
        
        # Test with method without docstring
        method = command_class.command_without_doc
        signature = inspect.signature(method)
        param = signature.parameters["param1"]
        
        help_text = self.cli._get_param_help(method.__doc__, param)
        self.assertEqual(help_text, None)

    def test_get_help(self):
        """Test _get_help method"""
        command_class = TestCommand
        method = command_class.command_with_doc
        
        help_text = self.cli._get_help(method.__doc__)
        self.assertEqual(help_text, "Test command with docstring")
        
        # Test with method without docstring
        method = command_class.command_without_doc
        help_text = self.cli._get_help(method.__doc__)
        self.assertEqual(help_text, None)

    def test_build_usage(self):
        """Test _build_usage method"""
        usage = self.cli._build_usage("command", "subcommand", ["arg1", "--option"])
        expected = "test_cli [args] command [args] subcommand arg1 --option"
        self.assertEqual(usage, expected)

    @patch.object(CliCore, "_get_plugin_modules")
    def test_parse(self, mock_get_plugin_modules):
        """Test parse method"""
        # Setup mock
        mock_get_plugin_modules.return_value = {}
        
        # Test with help flag
        args = ["-h"]
        with self.assertRaises(SystemExit):
            self.cli.parse(args)
        
        # Test with version flag
        args = ["-v"]
        self.cli.parse(args)
        self.assertTrue(self.cli.args._verbose)

    @patch.object(CliCore, "_add_subcommand_arguments")
    @patch.object(CliCore, "_get_plugin_modules")
    def test_run(self, mock_get_plugin_modules, mock_add_subcommand_args):
        """Test run method"""
        # Setup for command without subcommand
        mock_get_plugin_modules.return_value = {
            "test": {
                "plugin": MagicMock(),
                "command_classes": {
                    "TestCommand": TestCommand
                }
            }
        }
        
        # Create a mock namespace for args
        self.cli.args = argparse.Namespace()
        self.cli.args._command = "test"
        self.cli.args._command_class = "TestCommand"
        self.cli.args._subcommand = None
        
        # Run should create instance and call _handle_command
        with patch.object(self.cli, "_handle_command") as mock_handle_command:
            self.cli.run()
            mock_handle_command.assert_called_once()
            
        # Setup for command with subcommand
        self.cli.args._subcommand = "command_with_doc"
        
        # Run should create instance and call subcommand
        with patch.object(TestCommand, "command_with_doc") as mock_command:
            mock_command.return_value = None
            self.cli.run()
            mock_command.assert_called_once()


if __name__ == "__main__":
    unittest.main()