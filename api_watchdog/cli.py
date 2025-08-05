import argparse
from api_watchdog.utils.config import WeatherConfig, StockConfig


def parse_args():
    parser = argparse.ArgumentParser(description="CLI for API Watchdog")
    subparsers = parser.add_subparsers(dest="api")

    weather_parser = subparsers.add_parser("weather", help="Weather API")
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
        default="api_watchdog.log",
        help="File to log API responses to",
    )

    stock_parser = subparsers.add_parser("stock", help="Stock API")
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
        default="api_watchdog.log",
        help="File to log API responses to",
    )
    return parser.parse_args()
