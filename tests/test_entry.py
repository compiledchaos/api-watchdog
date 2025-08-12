"""Tests for the entry point module."""

import sys
import time
import threading
from unittest.mock import patch, MagicMock, ANY
import pytest

# Import the module to test
from api_watchdog.entry import run_cli, run_gui, monitor_api


class TestEntryPoint:
    """Test the entry point functionality."""

    @patch('api_watchdog.entry.parse_args')
    @patch('api_watchdog.entry.get_logger')
    @patch('api_watchdog.entry.time.sleep', side_effect=KeyboardInterrupt)
    @patch('api_watchdog.entry.fetch_api')
    def test_run_cli_keyboard_interrupt(self, mock_fetch_api, mock_sleep, mock_get_logger, mock_parse_args):
        """Test CLI mode with keyboard interrupt."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_console_log = MagicMock()
        mock_get_logger.side_effect = [mock_logger, mock_console_log]
        
        mock_args = MagicMock()
        mock_args.api = MagicMock()
        mock_args.api.var = "test_var"
        mock_args.interval = 5
        mock_args.log_file = "test.log"
        mock_parse_args.return_value = mock_args
        
        # Mock API response
        mock_fetch_api.return_value = {"test": "data"}
        
        # Test
        run_cli()
        
        # Verify
        mock_console_log.info.assert_any_call("Starting API Watchdog")
        mock_console_log.info.assert_any_call("Stopping API Watchdog")

    @patch('api_watchdog.entry.APIWatchdogGUI')
    @patch('api_watchdog.entry.tk.Tk')
    def test_run_gui(self, mock_tk, mock_gui_class):
        """Test GUI mode initialization."""
        # Setup mocks
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        mock_gui = MagicMock()
        mock_gui_class.return_value = mock_gui
        
        # Test
        run_gui()
        
        # Verify
        mock_tk.assert_called_once()
        mock_gui_class.assert_called_once_with(mock_root)
        mock_root.mainloop.assert_called_once()

    @patch('api_watchdog.entry.fetch_api')
    @patch('api_watchdog.entry.get_logger')
    @patch('api_watchdog.entry.threading')
    @patch('api_watchdog.entry.time')
    def test_monitor_api(self, mock_time, mock_threading, mock_get_logger, mock_fetch_api):
        """Test the monitor_api function."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Mock threading.Event
        mock_event = MagicMock()
        mock_event.is_set.side_effect = [False, True]  # First call returns False, then True
        mock_threading.Event.return_value = mock_event
        
        # Mock threading.Thread
        mock_thread = MagicMock()
        mock_threading.Thread.return_value = mock_thread
        
        # Mock API class and instance
        mock_api_instance = MagicMock()
        # Set up the api_url attribute as a property
        type(mock_api_instance).api_url = "http://test.api/endpoint"
        mock_api_class = MagicMock(return_value=mock_api_instance)
        mock_api_class.var = "test_arg"
        
        # Setup fetch_api response
        mock_fetch_api.return_value = {"test": "data"}
        
        # Create a mock for the root Tkinter object
        mock_root = MagicMock()
        
        # Call the function under test
        monitor_api(
            api_class=mock_api_class,
            interval=1,
            log_file="test.log",
            args={"test_arg": "value"},
            root=mock_root
        )
        
        # Verify the API class was instantiated correctly
        mock_api_class.assert_called_once_with(
            argument="value",
            logger=mock_logger,
            interval=1,
            log_file="test.log"
        )
        
        # Verify the thread was created and started
        mock_threading.Thread.assert_called_once()
        mock_thread.start.assert_called_once()
        
        # Verify fetch_api was called with the correct URL and retry parameters
        mock_fetch_api.assert_called_once()
        
        # Verify the API instance's configuration method was called
        assert mock_api_instance.configuration.called
        
        # Verify logging occurred
        assert mock_logger.info.called
