import argparse
from api_watchdog.utils.config import WeatherConfig, StockConfig


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the API Watchdog CLI.

    The CLI supports two subcommands: "weather" and "stock". The "weather"
    subcommand requires the --location argument and supports the --interval
    and --log-file arguments. The "stock" subcommand requires the --stock
    argument and supports the --interval and --log-file arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """

    parser = argparse.ArgumentParser(description="CLI for API Watchdog")
    subparsers = parser.add_subparsers(dest="api", required=True)

    weather_parser = subparsers.add_parser("weather", help="Monitor the weather API")
    weather_parser.set_defaults(api=WeatherConfig)
    weather_parser.add_argument(
        "--location",
        "-L",
        type=str,
        required=True,
        help="Location to monitor",
    )
    weather_parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=5,
        help="Interval between API calls in seconds",
    )
    weather_parser.add_argument(
        "--log-file",
        "-l",
        type=str,
        default="weather_api_watchdog.log",
        help="File to log API responses to",
    )

    stock_parser = subparsers.add_parser("stock", help="Monitor the stock API")
    stock_parser.set_defaults(api=StockConfig)
    stock_parser.add_argument(
        "--stock",
        "-s",
        type=str,
        required=True,
        help="Stock to monitor",
    )
    stock_parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=5,
        help="Interval between API calls in seconds",
    )
    stock_parser.add_argument(
        "--log-file",
        "-l",
        type=str,
        default="stock_api_watchdog.log",
        help="File to log API responses to",
    )

    parser.add_argument("--cli", "-c", action="store_true", help="Run in CLI mode")

    return parser.parse_args()
