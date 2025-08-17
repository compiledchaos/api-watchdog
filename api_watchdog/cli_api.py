from api_watchdog.utils.logger import get_logger
from api_watchdog.core_gui_and_cli.cli import parse_args
from api_watchdog.utils.api_fetcher import fetch_api
import time

def run_cli():
    """
    Run the API Watchdog command-line interface.

    This function will start the API Watchdog with the given command-line
    arguments. It will fetch the API data at the given interval and log the
    results to the file specified by --log-file.

    The function will exit if the user stops it with Ctrl+C.

    :raises Exception: If there is an error fetching the API data or writing
        the log file.
    """
    # Parse the command-line arguments once at startup
    args = parse_args()

    # Determine the API class that was chosen by the user (e.g. WeatherConfig
    # or StockConfig)
    api_class = args.api

    # Create a logger that will write to a file specified by the user, or
    # to the default log file if no file was specified
    log = get_logger(
        name="api_watchdog_file_cli", log_file=args.log_file, log_to_console=False
    )

    # Create a logger that will write to the console
    console_log = get_logger(
        name="api_watchdog_console_cli", log_to_console=True, log_to_file=False
    )

    # Start the API Watchdog
    console_log.info("Starting API Watchdog")

    # Determine the name of the argument that the user passed to the API
    # class (e.g. "location" for the Weather API, or "stock" for the Stock API)
    api_var = api_class.var

    # Create an instance of the API class with the user's arguments
    api = api_class(
        logger=log,
        argument=getattr(args, api_var),  # Get the argument from the args
        interval=args.interval,  # Get the interval from the args
        log_file=args.log_file,  # Get the log file from the args
    )

    # Get the API URL, interval, and log file from the API instance
    api_url, interval, _ = api.get_config()

    # Main loop of the program
    try:
        while True:
            # Log that we are fetching the API data
            console_log.info("Fetching API data...")

            try:
                # Fetch the API data
                api_data = fetch_api(api_url)

                # Pass the API data to the API class
                api.configuration(api_data)

                # Log that the API data was fetched successfully
                console_log.info("API data fetched successfully")
            except Exception as e:
                # Log that there was an error fetching the API data
                console_log.error(f"Error fetching API data: {e}")

            # Log that we are sleeping
            console_log.info(f"Sleeping for {interval} seconds...")

            # Sleep for the specified interval
            time.sleep(interval)
    except KeyboardInterrupt:
        # User stopped the program with Ctrl+C
        console_log.info("API Watchdog stopped by user")
    except Exception as e:
        # There was an error with the program
        console_log.error(f"API Watchdog stopped due to error: {e}")
