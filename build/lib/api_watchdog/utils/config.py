import os
from dotenv import load_dotenv
import json

load_dotenv()


class WeatherConfig:
    var = "location"

    def __init__(self, argument: str, logger, interval: int, log_file: str):
        self.api_url = f"https://api.openweathermap.org/data/2.5/weather?q={argument}&appid={os.getenv('OPENWEATHERMAP_API_KEY')}"
        self.interval = interval
        self.log_file = log_file
        self.log = logger

    def get_config(self):
        return self.api_url, self.interval, self.log_file

    def configuration(self, api_data):
        # api_data is already a parsed dictionary from fetch_api
        api = api_data

        self.log.info(f"Location: {api['name']}")
        self.log.info(f"Time: {api['dt']}")
        self.log.info(f"Country: {api['sys']['country']}")
        self.log.info(f"Weather: {api['weather'][0]['description']}")
        for a, b in zip(
            (
                "Wind speeds",
                "Wind direction",
                "Temperature",
                "Humidity",
                "Pressure",
                "Visibility",
                "Sunrise",
                "Sunset",
                "Clouds",
            ),
            (
                api["wind"]["speed"],
                api["wind"]["deg"],
                api["main"]["temp"],
                api["main"]["humidity"],
                api["main"]["pressure"],
                api["visibility"],
                api["sys"]["sunrise"],
                api["sys"]["sunset"],
                api["clouds"]["all"],
            ),
        ):
            try:
                self.log.info(f"{a}: {b}")
            except KeyError:
                self.log.info(f"{a}: Not available")

        self.log.info(f"API URL: {self.api_url}")
        self.log.info(f"Interval: {self.interval}")
        self.log.info(f"Log file: {self.log_file}")


class StockConfig:
    var = "stock"

    def __init__(self, argument: str, logger, interval: int, log_file: str):
        self.api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={argument}&interval={interval}min&apikey={os.getenv('ALPHAVANTAGE_API_KEY')}"
        self.interval = interval
        self.log_file = log_file
        self.log = logger

    def get_config(self):
        return self.api_url, self.interval, self.log_file

    def configuration(self, api_data):
        # api_data is already a parsed dictionary from fetch_api
        api = api_data

        # Check if API returned an error
        if "Error Message" in api:
            self.log.error(f"API Error: {api['Error Message']}")
            return
        if "Note" in api:
            self.log.error(f"API Limit: {api['Note']}")
            return
        if "Meta Data" not in api:
            self.log.error(f"Invalid API response: {list(api.keys())}")
            return

        self.log.info(f"Stock: {api['Meta Data']['2. Symbol']}")
        self.log.info(f"Time: {api['Meta Data']['3. Last Refreshed']}")

        # Use self.interval instead of undefined interval variable
        time_series_key = f"Time Series ({self.interval}min)"

        if time_series_key not in api:
            self.log.error(
                f"Time series data not found. Available keys: {list(api.keys())}"
            )
            return

        time_series = api[time_series_key]
        latest_time = list(time_series.keys())[0]
        latest_data = time_series[latest_time]

        self.log.info(f"Open: {latest_data['1. open']}")
        self.log.info(f"High: {latest_data['2. high']}")
        self.log.info(f"Low: {latest_data['3. low']}")
        self.log.info(f"Close: {latest_data['4. close']}")
        self.log.info(f"Volume: {latest_data['5. volume']}")

        self.log.info(f"API URL: {self.api_url}")
        self.log.info(f"Interval: {self.interval}")
        self.log.info(f"Log file: {self.log_file}")
