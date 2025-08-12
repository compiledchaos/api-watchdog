import os
from dotenv import load_dotenv
import time

load_dotenv()


class WeatherConfig:
    """
    Configuration for the Weather API.

    Attributes:
        var (str): The argument name for the API.
        api_url (str): The API URL.
        interval (int): The interval to fetch the API data.
        log_file (str): The log file to write the results to.
        log (logging.Logger): The logger to use for logging.

    Methods:
        get_config: Returns the API URL, interval, and log file.
        configuration: Logs the weather configuration.
    """

    var = "location"

    def __init__(self, argument: str, logger, interval: int, log_file: str):
        """
        Initialize the WeatherConfig instance.

        Args:
            argument (str): The argument to pass to the API.
            logger (logging.Logger): The logger to use for logging.
            interval (int): The interval to fetch the API data.
            log_file (str): The log file to write the results to.
        """
        self.api_url = f"https://api.openweathermap.org/data/2.5/weather?q={argument}&appid={os.getenv('OPENWEATHERMAP_API_KEY')}"
        self.interval = interval
        self.log_file = log_file
        self.log = logger

    def get_config(self) -> tuple:
        """
        Returns the API URL, interval, and log file.

        Returns:
            tuple: (api_url, interval, log_file)
        """
        return self.api_url, self.interval, self.log_file

    def configuration(self, api_data):
        """
        Logs the weather configuration.

        Args:
            api_data (dict): The parsed API response.
        """
        # Assign the parsed API data to a local variable for easier access
        api = api_data

        # Log the general location information
        self.log.info(f"Location: {api['name']}")
        # Log the current time in a human-readable format
        self.log.info(
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(api['dt']))}"
        )
        # Log the country code
        self.log.info(f"Country: {api['sys']['country']}")
        # Log the weather description
        self.log.info(f"Weather: {api['weather'][0]['description']}")

        # Create lists of attribute names and their corresponding values for logging
        attribute_names = (
            "Wind speeds",
            "Wind direction",
            "Temperature",
            "Humidity",
            "Pressure",
            "Visibility",
            "Sunrise",
            "Sunset",
            "Clouds",
        )
        attribute_values = (
            f"{api['wind']['speed']} m/s",  # Wind speed in meters per second
            f"{api['wind']['deg']}°",  # Wind direction in degrees
            f"{round(api['main']['temp'] - 273.15, 2)}°C",  # Temperature in Celsius
            f"{api['main']['humidity']}%",  # Humidity as a percentage
            f"{api['main']['pressure']} hPa",  # Pressure in hectopascals
            f"{api['visibility']} m",  # Visibility in meters
            # Sunrise time in a human-readable format
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(api["sys"]["sunrise"])),
            # Sunset time in a human-readable format
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(api["sys"]["sunset"])),
            f"{api['clouds']['all']}%",  # Cloudiness as a percentage
        )

        # Iterate over the attribute names and values to log each one
        for a, b in zip(attribute_names, attribute_values):
            try:
                # Log each attribute name and its corresponding value
                self.log.info(f"{a}: {b}")
            except KeyError:
                # If a KeyError occurs, log that the attribute is not available
                self.log.info(f"{a}: Not available")

        # Log the API URL being used
        self.log.info(f"API URL: {self.api_url}")
        # Log the interval at which the API is being polled
        self.log.info(f"Interval: {self.interval}")
        # Log the file where logs are being written
        self.log.info(f"Log file: {self.log_file}")
