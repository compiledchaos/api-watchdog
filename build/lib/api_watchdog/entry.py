from api_watchdog.utils.api_fetcher import fetch_api
from api_watchdog.utils.logger import get_logger
import time
from api_watchdog.cli import parse_args


def run():
    # Parse arguments once at startup
    args = parse_args()
    api_class = args.api
    log = get_logger(name="api_watchdog_file", log_file=args.log_file, log_to_console=False)
    console_log = get_logger(name="api_watchdog_console", log_to_console=True, log_to_file=False)

    console_log.info("Starting API Watchdog")
    api_var = api_class.var

    # Create API instance once
    api = api_class(
        logger=log,
        argument=getattr(args, api_var),
        interval=args.interval,
        log_file=args.log_file,
    )

    api_url, interval, _ = api.get_config()

    try:
        while True:
            console_log.info("Fetching API data...")
            try:
                api_data = fetch_api(api_url)
                api.configuration(api_data)
                console_log.info("API data fetched successfully")
            except Exception as e:
                console_log.error(f"Error fetching API data: {e}")

            console_log.info(f"Sleeping for {interval} seconds...")
            time.sleep(interval)
    except KeyboardInterrupt:
        console_log.info("API Watchdog stopped by user")
    except Exception as e:
        console_log.error(f"API Watchdog stopped due to error: {e}")


if __name__ == "__main__":
    run()
