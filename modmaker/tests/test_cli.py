"""
Unit tests for _cli.py
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import argparse

# Import module under test
from modmaker._cli import (
    _get_log_level,
    _print_tracebacks,
    _setup_logging,
    SetVerbosity,
    get_installed_version,
    get_pip_version,
    main,
    NAME,
)


class TestCli(unittest.TestCase):
    """Test cases for CLI module"""

    def test_get_log_level_default(self):
        """Test default log level"""
        args = []
        self.assertEqual(_get_log_level(args), "INFO")

    def test_get_log_level_debug(self):
        """Test debug log level"""
        args = ["--debug"]
        self.assertEqual(_get_log_level(args), "DEBUG")
        args = ["-d"]
        self.assertEqual(_get_log_level(args), "DEBUG")

    def test_get_log_level_quiet(self):
        """Test quiet log level"""
        args = ["--quiet"]
        self.assertEqual(_get_log_level(args), "ERROR")
        args = ["-q"]
        self.assertEqual(_get_log_level(args), "ERROR")

    def test_get_log_level_conflict(self):
        """Test conflict between debug and quiet"""
        args = ["--debug", "--quiet"]
        exit_func = MagicMock()
        _get_log_level(args, exit_func=exit_func)
        exit_func.assert_called_once_with(1, "--debug and --quiet cannot be specified simultaneously")

    def test_print_tracebacks(self):
        """Test traceback printing logic"""
        self.assertTrue(_print_tracebacks("DEBUG"))
        self.assertFalse(_print_tracebacks("INFO"))
        self.assertFalse(_print_tracebacks("ERROR"))

    @patch("modmaker._cli.get_distribution_version")
    def test_get_installed_version_success(self, mock_get_version):
        """Test successful version retrieval"""
        mock_get_version.return_value = "1.0.0"
        self.assertEqual(get_installed_version(), "1.0.0")
        mock_get_version.assert_called_once_with(NAME)

    @patch("modmaker._cli.get_distribution_version")
    def test_get_installed_version_error(self, mock_get_version):
        """Test version retrieval error handling"""
        mock_get_version.side_effect = Exception("Test error")
        self.assertEqual(get_installed_version(), "[local source] no pip module installed")

    @patch("modmaker._cli.requests.get")
    def test_get_pip_version(self, mock_get):
        """Test PyPI version retrieval"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"info": {"version": "1.0.0"}}
        mock_get.return_value = mock_response
        
        url = "https://pypi.org/pypi/modmaker/json"
        self.assertEqual(get_pip_version(url), "1.0.0")
        mock_get.assert_called_once_with(url, timeout=5.0)

    @patch("modmaker._cli.signal.signal")
    @patch("modmaker._cli._setup_logging")
    @patch("modmaker._cli._welcome")
    @patch("modmaker._cli.get_installed_version")
    @patch("modmaker._cli.CliCore")
    def test_main_success(self, mock_cli_core, mock_get_version, mock_welcome, 
                          mock_setup_logging, mock_signal):
        """Test successful CLI execution"""
        # Setup
        mock_cli_instance = MagicMock()
        mock_cli_core.return_value = mock_cli_instance
        mock_get_version.return_value = "1.0.0"
        mock_setup_logging.return_value = "INFO"
        
        # Save and restore sys.argv
        old_argv = sys.argv
        sys.argv = ["modmaker", "command", "--option"]
        
        try:
            # Execute
            exit_func = MagicMock()
            main(exit_func=exit_func)
            
            # Verify
            mock_welcome.assert_called_once()
            mock_get_version.assert_called_once()
            mock_cli_core.assert_called_once()
            mock_cli_instance.parse.assert_called_once_with(["command", "--option"])
            mock_cli_instance.run.assert_called_once()
            exit_func.assert_not_called()
        finally:
            # Restore
            sys.argv = old_argv

    @patch("modmaker._cli._welcome")
    def test_main_exception(self, mock_welcome):
        """Test CLI execution with exception"""
        # Setup
        mock_welcome.side_effect = Exception("Test error")
        
        # Save and restore sys.argv
        old_argv = sys.argv
        sys.argv = ["modmaker", "command"]
        
        try:
            # Execute
            exit_func = MagicMock()
            main(exit_func=exit_func)
            
            # Verify
            exit_func.assert_called_once_with(1)
        finally:
            # Restore
            sys.argv = old_argv


if __name__ == "__main__":
    unittest.main()