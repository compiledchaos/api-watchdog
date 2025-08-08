import requests as req


def fetch_api(api_url):
    """
    Fetch data from the given API URL and return its JSON content.

    Args:
        api_url (str): The URL of the API to fetch data from.

    Returns:
        dict: The JSON content returned by the API.
    """
    response = req.get(api_url)
    return response.json()
