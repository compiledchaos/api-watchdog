"""Tests for the GUI module."""

import tkinter as tk
import threading
from unittest.mock import patch, MagicMock, ANY, PropertyMock
import pytest

# Import the module to test
from api_watchdog.gui import APIWatchdogGUI

# Create a mock for the messagebox
class MockMessageBox:
    @staticmethod
    def showerror(title=None, message=None, **kwargs):
        pass

# Patch the messagebox and threading at the module level
import api_watchdog.gui as gui_module
gui_module.messagebox = MockMessageBox()

# Mock threading for tests
class MockThread:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._is_alive = True
        
    def start(self):
        pass
        
    def is_alive(self):
        return self._is_alive
        
    def join(self, timeout=None):
        self._is_alive = False

gui_module.threading.Thread = MockThread


class TestAPIWatchdogGUI:
    """Test the APIWatchdogGUI class."""

    @patch("api_watchdog.gui.ttk.Frame")
    @patch("api_watchdog.gui.ttk.Label")
    @patch("api_watchdog.gui.api_selector")
    @patch("api_watchdog.gui.interval_selector")
    @patch("api_watchdog.gui.log_file_selector")
    @patch("api_watchdog.gui.select_api_args")
    def test_init(
        self,
        mock_select_api_args,
        mock_log_file_selector,
        mock_interval_selector,
        mock_api_selector,
        mock_label,
        mock_frame,
    ):
        """Test GUI initialization."""
        # Setup mocks
        mock_root = MagicMock()
        mock_frame_instance = MagicMock()
        mock_frame.return_value = mock_frame_instance

        # Test
        gui = APIWatchdogGUI(mock_root)

        # Verify
        mock_frame.assert_called_once_with(mock_root)
        mock_frame_instance.grid.assert_called_once_with(
            column=0, row=0, sticky=("W", "N", "E", "S")
        )
        mock_root.title.assert_called_once_with("API Watchdog")

    @patch("api_watchdog.gui.APIWatchdogGUI.setup_ui")
    @patch("api_watchdog.gui.threading.Thread")
    def test_start_stop(self, mock_thread, mock_setup_ui):
        """Test start and stop functionality."""
        # Setup
        mock_root = MagicMock()
        
        # Configure mocks
        gui = APIWatchdogGUI(mock_root)
        gui.start_button = MagicMock()
        gui.set_button = MagicMock()
        gui.started = False
        
        # Mock validate_entries to return True
        with patch.object(gui, 'validate_entries', return_value=True):
            # Test start
            gui.start()
            assert gui.started is True
            gui.start_button.config.assert_called_with(text="Stop")
            
            # Reset the button mock for the stop test
            gui.start_button.reset_mock()
            
            # Test stop
            gui.stop()
            assert gui.started is False
            gui.start_button.config.assert_called_with(text="Start")

    @patch("api_watchdog.gui.APIWatchdogGUI.setup_ui")
    @patch("api_watchdog.gui.messagebox.showerror")
    def test_validate_entries_missing_fields(self, mock_showerror, mock_setup_ui):
        """Test validation with missing interval field."""
        # Setup
        mock_root = MagicMock()
        gui = APIWatchdogGUI(mock_root)
        gui.api_type = MagicMock()
        gui.api_type.get.return_value = "Weather"
        gui.interval = MagicMock()
        gui.interval.get.return_value = ""  # Empty interval
        
        # Add log file mock
        gui.log_file = MagicMock()
        gui.log_file.get.return_value = "test.log"
        
        # Add API entries
        gui.api_entries = []

        # Test
        result = gui.validate_entries()

        # Verify
        assert result is False
        mock_showerror.assert_called_once_with("Error", "Please enter an interval")

    @patch("api_watchdog.gui.APIWatchdogGUI.setup_ui")
    @patch("api_watchdog.gui.messagebox.showerror")
    def test_validate_entries_invalid_interval(self, mock_showerror, mock_setup_ui):
        """Test validation with invalid interval."""
        # Setup
        mock_root = MagicMock()
        gui = APIWatchdogGUI(mock_root)
        gui.api_type = MagicMock()
        gui.api_type.get.return_value = "Weather"
        gui.interval = MagicMock()
        gui.interval.get.return_value = "not_a_number"  # Invalid interval
        
        # Add log file mock
        gui.log_file = MagicMock()
        gui.log_file.get.return_value = "test.log"
        
        # Add API entries
        gui.api_entries = []

        # Test
        result = gui.validate_entries()

        # Verify
        assert result is False
        mock_showerror.assert_called_once_with("Error", "Interval must be a positive number")
