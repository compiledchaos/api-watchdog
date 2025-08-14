from api_watchdog.core_gui_and_cli.gui import APIWatchdogGUI
from api_watchdog.utils.gui_utils import stop_button
from api_watchdog.monitor_api_gui import monitor_api
from threading import Thread
import tkinter as tk
from api_watchdog.utils.logger import get_logger


def run_gui():
    """Run the API Watchdog GUI application."""
    # Initialize the GUI
    root = tk.Tk()
    app = APIWatchdogGUI(root)
    logger = get_logger("api_watchdog", log_to_console=True, log_to_file=False)

    def stop_button_clicked():
        """Stop the GUI."""
        logger.info("Stopping GUI...")
        root.quit()

    def on_start():
        """Start monitoring the API in a separate thread."""
        # Get GUI arguments
        try:
            api_class, interval, log_file, args = app.get_args()

            # Start monitoring in a separate thread
            monitor_thread = Thread(
                target=monitor_api,
                args=(api_class, interval, log_file, args, root),
                daemon=True,
            )
            monitor_thread.start()
            app.started = True
        except Exception as e:
            logger.error(f"Error starting monitoring: {e}")

    # Update the start button command
    app.start_button.config(command=on_start)
    stop_button(app.frame, command=stop_button_clicked)
    # Start the GUI
    root.mainloop()
