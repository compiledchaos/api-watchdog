import os
from dotenv import load_dotenv

load_dotenv()


class StockConfig:
    """
    A class that encapsulates the configuration for the stock price API request
    """

    var = "stock"

    def __init__(self, argument: str, logger, interval: int, log_file: str):
        """
        Constructor for the StockConfig class

        Args:
            argument (str): The stock symbol to query
            logger: The logger to use for logging
            interval (int): The interval at which to query the API
            log_file (str): The file to write the logs to
        """
        self.api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={argument}&interval={interval}min&apikey={os.getenv('ALPHAVANTAGE_API_KEY')}"
        self.interval = interval
        self.log_file = log_file
        self.log = logger

    def get_config(self) -> tuple:
        """
        Returns a tuple containing the API URL, interval, and log file
        """
        return self.api_url, self.interval, self.log_file

    def configuration(self, api_data):
        """
        Logs the configuration for the stock price API request

        Args:
            api_data (dict): The parsed API response
        """
        # api_data is already a parsed dictionary from fetch_api
        api = api_data

        # Check if API returned an error
        if "Error Message" in api:
            self.log.error(f"API Error: {api['Error Message']}")
            self.log.debug(f"Full API response: {api}")
            return
        if "Note" in api:
            self.log.error(f"API Limit: {api['Note']}")
            self.log.debug(f"Full API response: {api}")
            return
        if "Meta Data" not in api:
            self.log.error(f"Invalid API response: {list(api.keys())}")
            self.log.debug(f"Full API response: {api}")
            return

        # Log the stock symbol
        self.log.info(f"Stock: {api['Meta Data']['2. Symbol']}")

        # Log the time of the latest data
        self.log.info(f"Time: {api['Meta Data']['3. Last Refreshed']}")

        # Get the time series key based on the interval
        time_series_key = f"Time Series ({self.interval}min)"

        # Check if the time series key is in the API response
        if time_series_key not in api:
            self.log.error(
                f"Time series data not found. Available keys: {list(api.keys())}"
            )
            self.log.debug(f"Full API response: {api}")
            return

        # Get the time series data
        time_series = api[time_series_key]

        # Get the latest time and data
        latest_time = list(time_series.keys())[0]
        latest_data = time_series[latest_time]

        # Log the latest data
        self.log.info(f"Open: {latest_data['1. open']}")
        self.log.info(f"High: {latest_data['2. high']}")
        self.log.info(f"Low: {latest_data['3. low']}")
        self.log.info(f"Close: {latest_data['4. close']}")
        self.log.info(f"Volume: {latest_data['5. volume']}")

        # Log the API URL being used
        self.log.info(f"API URL: {self.api_url}")

        # Log the interval at which the API is being polled
        self.log.info(f"Interval: {self.interval}")

        # Log the file where logs are being written
        self.log.info(f"Log file: {self.log_file}")
