import requests
import time
from api_watchdog.utils.logger import get_logger


def fetch_api(api_url, max_retries=5, delay=5):
    """
    Fetch data from the given API URL and return its JSON content.

    Args:
        api_url (str): The URL of the API to fetch data from.

    Returns:
        dict: The JSON content returned by the API.
    """
    logger = get_logger(name="api_fetcher", log_to_console=True, log_to_file=False)
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(api_url, timeout=10)  # timeout to avoid hanging
            response.raise_for_status()  # raises error for 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(
                f"[Attempt {attempt}/{max_retries}] Error fetching API data: {e}"
            )
            if attempt < max_retries:
                time.sleep(delay)
    return None
