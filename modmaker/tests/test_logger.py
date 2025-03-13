"""
Unit tests for _logger.py
"""

import unittest
from unittest.mock import patch, MagicMock
import logging

# Import module under test
from modmaker._logger import (
    init_modmaker_cli_logger,
    AppFilter,
)


class TestLogger(unittest.TestCase):
    """Test cases for logger module"""

    def test_app_filter(self):
        """Test AppFilter class"""
        # Create a test record
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Apply filter
        app_filter = AppFilter()
        filtered_record = app_filter.filter(record)
        
        # Check that record is returned and modified
        self.assertEqual(filtered_record, record)
        self.assertEqual(record.pathname, "test_logger")

    @patch("logging.getLogger")
    def test_init_modmaker_cli_logger_default(self, mock_getLogger):
        """Test logger initialization with default settings"""
        mock_logger = MagicMock()
        mock_getLogger.return_value = mock_logger
        
        # Call with default loglevel
        logger = init_modmaker_cli_logger()
        
        # Verify logger setup
        mock_getLogger.assert_called_once_with("modmaker")
        self.assertEqual(logger, mock_logger)
        mock_logger.setLevel.assert_called_once_with("ERROR")
        self.assertEqual(mock_logger.handlers[0].level, logging.ERROR)

    @patch("logging.getLogger")
    def test_init_modmaker_cli_logger_custom_level(self, mock_getLogger):
        """Test logger initialization with custom log level"""
        mock_logger = MagicMock()
        mock_getLogger.return_value = mock_logger
        
        # Call with custom loglevel
        logger = init_modmaker_cli_logger(loglevel="DEBUG")
        
        # Verify logger setup
        mock_getLogger.assert_called_once_with("modmaker")
        self.assertEqual(logger, mock_logger)
        mock_logger.setLevel.assert_called_once_with("DEBUG")
        self.assertEqual(mock_logger.handlers[0].level, logging.DEBUG)

    @patch("logging.getLogger")
    def test_init_modmaker_cli_logger_invalid_level(self, mock_getLogger):
        """Test logger initialization with invalid log level"""
        mock_logger = MagicMock()
        mock_getLogger.return_value = mock_logger
        
        # Should default to ERROR if invalid level is provided
        logger = init_modmaker_cli_logger(loglevel="INVALID")
        
        # Verify logger setup
        mock_getLogger.assert_called_once_with("modmaker")
        self.assertEqual(logger, mock_logger)
        mock_logger.setLevel.assert_called_once_with("ERROR")
        self.assertEqual(mock_logger.handlers[0].level, logging.ERROR)


if __name__ == "__main__":
    unittest.main()