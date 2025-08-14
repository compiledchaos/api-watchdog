from api_watchdog.utils.api_fetcher import fetch_api
from api_watchdog.utils.logger import get_logger
from pathlib import Path
import hashlib


def monitor_api(api_class, interval, log_file, args, root):
    """
    Run the API monitoring in a separate thread.

    Parameters
    ----------
    api_class : type
        The class of the API to monitor.
    interval : int
        The interval in seconds at which to update the API data.
    log_file : str or None
        The path to the log file to write to, or None to use the default.
    args : list of str
        The command line arguments to pass to the API class.
    root : tk.Tk
        The root Tk widget of the GUI.

    Notes
    -----
    This function creates an API instance and starts a loop that fetches the API
    data at the specified interval and updates the GUI accordingly. If there is
    an error fetching the API data, it logs the error and continues to the next
    iteration. If there is an error in the loop itself, it logs the error and
    exits.
    """

    try:
        # Ensure that the 'logs' directory exists, creating it if necessary
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Set the default log file path within the 'logs' directory
        log_file_path = str(logs_dir / "api_watchdog.log")

        # Use the provided log file path if it is valid, otherwise use the default
        if log_file and isinstance(log_file, str) and log_file.strip():
            log_file_path = log_file.strip()

        # Create a unique logger name based on the log file path
        log_name = f"api_watchdog_{hashlib.md5(log_file_path.encode()).hexdigest()[:8]}"

        # Initialize a logger for writing logs to file
        log = get_logger(name=log_name, log_file=log_file_path, log_to_console=False)
        # Initialize a separate logger for console output
        console_log = get_logger(
            name=f"{log_name}_console", log_to_console=True, log_to_file=False
        )

        # Create an instance of the API class with the provided arguments
        api = api_class(
            logger=log,
            argument=(
                args[0] if args else ""
            ),  # Use the first argument or an empty string
            interval=(
                int(interval) if interval and interval.isdigit() else 60
            ),  # Use the provided interval or default to 60 seconds
            log_file=log_file_path,
        )

        # Retrieve the API URL, interval, and log file path from the API instance
        api_url, interval, _ = api.get_config()

        def fetch_and_update():
            """Fetch API data and update the application."""
            try:
                # Log the start of the API data fetching process
                console_log.info("Fetching API data...")
                try:
                    # Attempt to fetch the API data using the provided URL
                    api_data = fetch_api(api_url)

                    # Pass the fetched data to the API class for processing
                    api.configuration(api_data)

                    # Log successful fetching and configuration of API data
                    console_log.info("API data fetched successfully")
                except Exception as e:
                    # Log any errors encountered during the fetching process
                    console_log.error(f"Error fetching API data: {e}")

                # Schedule the next API data fetch after a specified interval
                # Convert interval from seconds to milliseconds for tkinter's after method
                root.after(int(interval) * 1000, fetch_and_update)

            except Exception as e:
                # Log any errors encountered during the monitoring process
                console_log.error(f"Error in API monitoring: {e}")

        # Start the monitoring loop by calling the fetch_and_update function
        fetch_and_update()

    except TypeError:
        console_log.error("API monitoring failed to start: No API class provided")

    except Exception as e:
        # Initialize a console logger if an error occurs during setup
        console_log = get_logger(
            name="api_watchdog_console_gui", log_to_console=True, log_to_file=False
        )
        # Log the error indicating the failure to start API monitoring
        console_log.error(f"API monitoring failed to start: {e}")
