import requests as req


def fetch_api(api_url):
    response = req.get(api_url)
    return response.json()
