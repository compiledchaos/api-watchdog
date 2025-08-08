"""Tests for the logger utility."""
import os
import logging
import tempfile
from pathlib import Path

import pytest

from api_watchdog.utils.logger import get_logger


def test_logger_creates_file(tmp_path):
    """Test that logger creates a log file when initialized."""
    log_file = tmp_path / "test.log"
    logger = get_logger("test_logger", log_to_file=True, log_file=str(log_file))
    
    test_message = "Test log message"
    logger.info(test_message)
    
    # Ensure the log file was created
    assert log_file.exists()
    
    # Read the log file and check if it contains our test message
    log_content = log_file.read_text(encoding='utf-8')
    assert test_message in log_content
    
    # Clean up logger handlers
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def test_logger_format(tmp_path):
    """Test that logger uses the correct format."""
    log_file = tmp_path / "format_test.log"
    logger = get_logger("format_test_logger", log_to_file=True, log_file=str(log_file))
    
    test_message = "Format test message"
    logger.info(test_message)
    
    # Ensure all handlers have processed the message
    for handler in logger.handlers:
        handler.flush()
    
    log_content = log_file.read_text(encoding='utf-8').strip()
    
    # Check the format: [timestamp] LEVEL: message function_name
    assert 'INFO: ' in log_content
    assert test_message in log_content
    
    # Check timestamp format (YYYY-MM-DD HH:MM:SS)
    import re
    timestamp_pattern = r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'
    assert re.search(timestamp_pattern, log_content) is not None
    
    # Clean up logger handlers
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def test_logger_different_levels(tmp_path):
    """Test that different log levels work as expected."""
    log_file = tmp_path / "levels_test.log"
    logger = get_logger("levels_test_logger", log_to_file=True, log_file=str(log_file))
    
    # Set level to DEBUG to capture all messages
    logger.setLevel(logging.DEBUG)
    
    debug_msg = "Debug message"
    info_msg = "Info message"
    warning_msg = "Warning message"
    error_msg = "Error message"
    
    logger.debug(debug_msg)
    logger.info(info_msg)
    logger.warning(warning_msg)
    logger.error(error_msg)
    
    # Ensure all handlers have processed the messages
    for handler in logger.handlers:
        handler.flush()
    
    log_content = log_file.read_text(encoding='utf-8')
        
    # Check that all messages are in the log
    assert debug_msg in log_content
    assert info_msg in log_content
    assert warning_msg in log_content
    assert error_msg in log_content
    
    # Clean up logger handlers
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def test_console_logging(capsys):
    """Test that console logging works when enabled."""
    logger = get_logger("console_test_logger", log_to_console=True)
    test_message = "This should appear in console"
    
    logger.info(test_message)
    
    # Capture stdout and stderr
    captured = capsys.readouterr()
    assert test_message in captured.out or test_message in captured.err
