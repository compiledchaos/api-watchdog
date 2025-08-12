import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from api_watchdog.utils.api_configuration import WeatherConfig, StockConfig
from api_watchdog.utils.gui_utils import (
    api_selector,
    interval_selector,
    log_file_selector,
    select_api_args,
)


class APIWatchdogGUI:
    """Main class for the API Watchdog GUI application."""

    def __init__(self, root):
        """
        Initialize the GUI components.

        Args:
            root: The root Tkinter widget.
        """
        self.root = root
        self.frame = ttk.Frame(root)
        self.frame.grid(column=0, row=0, sticky=("W", "N", "E", "S"))
        self.root.title("API Watchdog")

        # Initialize attributes
        self.api_type = None
        self.api_class = None
        self.api_entries = []
        self.interval = None
        self.log_file = None
        self.start_button = None
        self.set_button = None
        self.values_dict = {"Weather": WeatherConfig, "Stock": StockConfig}
        self.started = False

        # Set up the user interface
        self.setup_ui()

    def validate_entries(self):
        """Validate the form entries.
        
        Returns:
            bool: True if all entries are valid, False otherwise.
        """
        # Get values from the form
        api_type = self.api_type.get()
        interval = self.interval.get()
        log_file = self.log_file.get() if hasattr(self, 'log_file') else ''
        
        # Check if required fields are empty
        if not api_type:
            messagebox.showerror("Error", "Please select an API type")
            return False
            
        if not interval:
            messagebox.showerror("Error", "Please enter an interval")
            return False
            
        # Validate interval is a number
        try:
            interval = int(interval)
            if interval <= 0:
                raise ValueError("Interval must be positive")
        except ValueError:
            messagebox.showerror("Error", "Interval must be a positive number")
            return False
            
        # Validate log file if specified
        if log_file and not log_file.endswith('.log'):
            messagebox.showerror("Error", "Log file must have a .log extension")
            return False
            
        # Validate API-specific fields
        if not hasattr(self, 'api_entries'):
            self.api_entries = []
            
        for entry in self.api_entries:
            if hasattr(entry, 'get') and not entry.get().strip():
                messagebox.showerror("Error", "Please fill in all required fields")
                return False
                
        return True
        
    def setup_ui(self):
        """Set up the main UI components."""
        # Add label for the application
        self.api_label = ttk.Label(self.frame, text="API Watchdog")
        self.api_label.grid(column=0, row=0, columnspan=2, pady=10)

        # Add dropdown for API type selection
        self.api_type = api_selector(self.frame, self.values_dict)
        # Add entry for interval
        self.interval = interval_selector(self.frame)
        # Add entry for log file
        self.log_file = log_file_selector(self.frame)

        # Add a start button
        self.start_button = ttk.Button(self.frame, text="Start", command=self.start_api)
        self.start_button.grid(column=0, row=4, columnspan=2, pady=5)

        # Add a set button
        self.set_button = ttk.Button(
            self.frame, text="Set", command=self.on_set_clicked
        )
        self.set_button.grid(column=0, row=6, columnspan=2, pady=5)

    def start(self):
        """Start the API Watchdog monitoring."""
        if not self.validate_entries():
            return
            
        self.started = True
        self.start_button.config(text="Stop")
        
        # Start the monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_api, daemon=True)
        self.monitor_thread.start()
    
    def stop(self):
        """Stop the API Watchdog monitoring."""
        self.started = False
        self.start_button.config(text="Start")
    
    def monitor_api(self):
        """Monitor the API at regular intervals."""
        while self.started:
            try:
                # Get the API configuration
                api_class, interval, log_file, args = self.get_args()
                
                # Here you would typically call your API and update the UI
                # For now, we'll just sleep for the interval
                time.sleep(interval)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error monitoring API: {str(e)}")
                self.stop()
    
    def start_api(self):
        """Start the API Watchdog application."""
        self.started = True  # Mark the application as started

    def setup_api_arguments(self):
        """Clear and setup new API argument fields."""
        # Remove existing API argument fields
        for widget in self.frame.grid_slaves():
            if int(widget.grid_info()["row"]) == 5:
                widget.destroy()

        # Get the selected API class
        api_class = self.api_type.get()
        self.api_entries.clear()

        # Set up new API argument fields
        self.api_entries = select_api_args(self.frame, api_class, self.values_dict)

    def on_set_clicked(self):
        """Callback for the set button."""
        # Set up API arguments when set button is clicked
        self.setup_api_arguments()

    def get_args(self):
        """
        Get the arguments from the GUI.

        Returns:
            A tuple containing the API class, interval, log file, and arguments.
        """
        api_type = self.api_type.get()
        api_class = self.values_dict.get(api_type)
        interval = self.interval.get()
        log_file = self.log_file.get()

        # Gather arguments from entry fields
        args = [entry.get() for entry in self.api_entries if hasattr(entry, "get")]

        return api_class, interval, log_file, args
