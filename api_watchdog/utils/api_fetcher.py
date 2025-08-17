import requests
import time
from api_watchdog.utils.logger import get_logger


def fetch_api(api_url, max_retries=5, delay=5):
    """
    Fetch data from the given API URL and return its JSON content.

    This function handles the following scenarios:

    1. The API request fails with a 4XX or 5XX status code.
    2. The API request fails with a connection error or timeout.
    3. The API request fails after some number of retries.

    Args:
        api_url (str): The URL of the API to fetch data from.
        max_retries (int): The maximum number of times to retry fetching the API data.
        delay (int): The delay in seconds between retry attempts.

    Returns:
        dict: The JSON content returned by the API, or None if the fetch fails.
    """
    # Get a logger to log errors
    logger = get_logger(name="api_fetcher", log_to_console=True, log_to_file=False)

    # Set up a loop to retry the API fetch if it fails
    for attempt in range(1, max_retries + 1):
        try:
            # Send a GET request to the API
            response = requests.get(api_url, timeout=10)  # timeout to avoid hanging

            # Raise an error if the request was unsuccessful
            response.raise_for_status()  # raise HTTPError for 4XX/5XX responses

            # Return the JSON content of the response
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Log the error if the request was unsuccessful
            logger.error(f"[Attempt {attempt}/{max_retries}] HTTP Error: {http_err}")
            # If this is the last retry, raise the error
            if attempt == max_retries:
                raise
        except requests.exceptions.RequestException as e:
            # Log the error if the request failed for any other reason
            logger.error(
                f"[Attempt {attempt}/{max_retries}] Error fetching API data: {e}"
            )
            # If this is the last retry, raise the error
            if attempt == max_retries:
                raise

        # Sleep for the specified delay before retrying
        time.sleep(delay)  # wait before retrying

    # If all retries failed, return None
    return None
