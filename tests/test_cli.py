"""Tests for the CLI module."""

import sys
import argparse
import os
from unittest.mock import patch, MagicMock, ANY
import pytest

# Import the module to test
from api_watchdog.cli import parse_args


@patch.dict(os.environ, {"OPENWEATHERMAP_API_KEY": "test_key", "ALPHAVANTAGE_API_KEY": "test_key"})
def test_parse_args_weather():
    """Test parsing weather command line arguments."""
    test_args = ["weather", "--location", "London,uk", "--interval", "10", "--log-file", "test.log"]
    with patch.object(sys, 'argv', ["script.py"] + test_args):
        args = parse_args()
        
        assert args.api is not None
        assert args.location == "London,uk"
        assert args.interval == 10
        assert args.log_file == "test.log"


@patch.dict(os.environ, {"OPENWEATHERMAP_API_KEY": "test_key", "ALPHAVANTAGE_API_KEY": "test_key"})
def test_parse_args_stock():
    """Test parsing stock command line arguments."""
    test_args = ["stock", "--stock", "AAPL", "--interval", "5", "--log-file", "stock_test.log"]
    with patch.object(sys, 'argv', ["script.py"] + test_args):
        args = parse_args()
        
        assert args.api is not None
        assert args.stock == "AAPL"
        assert args.interval == 5
        assert args.log_file == "stock_test.log"


@patch.dict(os.environ, {"OPENWEATHERMAP_API_KEY": "test_key", "ALPHAVANTAGE_API_KEY": "test_key"})
def test_parse_args_defaults():
    """Test parsing with default values."""
    test_args = ["weather", "--location", "New York"]
    with patch.object(sys, 'argv', ["script.py"] + test_args):
        args = parse_args()
        
        assert args.location == "New York"
        assert args.interval == 5  # Default value
        assert args.log_file == "weather_api_watchdog.log"  # Default value


@patch.dict(os.environ, {"OPENWEATHERMAP_API_KEY": "test_key", "ALPHAVANTAGE_API_KEY": "test_key"})
@patch('sys.stderr')
@patch('sys.exit')
def test_parse_args_missing_required(mock_exit, mock_stderr):
    """Test missing required arguments."""
    test_args = ["weather"]  # Missing --location
    with patch.object(sys, 'argv', ["script.py"] + test_args):
        mock_exit.side_effect = SystemExit(2)
        with pytest.raises(SystemExit):
            parse_args()
        mock_exit.assert_called_once_with(2)


@patch.dict(os.environ, {"OPENWEATHERMAP_API_KEY": "test_key", "ALPHAVANTAGE_API_KEY": "test_key"})
def test_parse_args_cli_flag():
    """Test the --log-file flag."""
    test_args = ["weather", "--location", "Tokyo", "--log-file", "custom.log"]
    with patch.object(sys, 'argv', ["script.py"] + test_args):
        args = parse_args()
        assert args.log_file == "custom.log"
