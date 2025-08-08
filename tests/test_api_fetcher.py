"""Tests for the API fetcher utility."""

import json
from unittest.mock import patch, MagicMock
import pytest
import requests
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

from api_watchdog.utils.api_fetcher import fetch_api


class MockResponse:
    """Mock response for requests.get."""

    def __init__(self, json_data, status_code=200, text=None):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text or json.dumps(json_data)
        self._content = self.text.encode("utf-8")

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            http_error = HTTPError(f"HTTP Error {self.status_code}")
            http_error.response = self
            raise http_error
        return None


@patch("api_watchdog.utils.api_fetcher.req.get")
def test_fetch_success(mock_get):
    """Test successful API fetch."""
    # Setup mock response
    test_data = {"key": "value"}
    mock_response = MockResponse(test_data)
    mock_get.return_value = mock_response

    # Test
    result = fetch_api("http://test-api.com")

    # Verify
    assert result == test_data
    mock_get.assert_called_once_with("http://test-api.com")


@patch("api_watchdog.utils.api_fetcher.req.get")
def test_fetch_http_error(mock_get):
    """Test API fetch with HTTP error."""
    # Create a mock response with error status code
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = '{"error": "Not found"}'
    mock_response.json.return_value = {"error": "Not found"}

    mock_get.return_value = mock_response

    # Test and verify
    result = fetch_api("http://test-api.com/not-found")

    # The function should return the JSON response even for error status codes
    assert result == {"error": "Not found"}
    mock_get.assert_called_once_with("http://test-api.com/not-found")


@patch("api_watchdog.utils.api_fetcher.req.get")
def test_fetch_connection_error(mock_get):
    """Test API fetch with connection error."""
    # Setup mock to raise ConnectionError
    mock_get.side_effect = ConnectionError("Connection failed")

    # Test and verify
    with pytest.raises(ConnectionError) as exc_info:
        fetch_api("http://unreachable-api.com")

    assert "Connection failed" in str(exc_info.value)
    mock_get.assert_called_once_with("http://unreachable-api.com")


@patch("api_watchdog.utils.api_fetcher.req.get")
def test_fetch_timeout(mock_get):
    """Test API fetch with timeout."""
    # Setup mock to raise Timeout
    mock_get.side_effect = Timeout("Request timed out")

    # Test and verify
    with pytest.raises(Timeout) as exc_info:
        fetch_api("http://slow-api.com")

    assert "timed out" in str(exc_info.value).lower()
    mock_get.assert_called_once_with("http://slow-api.com")


@patch("api_watchdog.utils.api_fetcher.req.get")
def test_fetch_invalid_json(mock_get):
    """Test API fetch with invalid JSON response."""

    # Setup mock with invalid JSON
    class InvalidJSONResponse:
        def __init__(self):
            self.status_code = 200
            self.text = "not a json"
            self._content = self.text.encode("utf-8")

        def json(self):
            raise json.JSONDecodeError("Expecting value", "not a json", 0)

        def raise_for_status(self):
            pass

    mock_get.return_value = InvalidJSONResponse()

    # Test and verify
    with pytest.raises(json.JSONDecodeError) as exc_info:
        fetch_api("http://api-with-invalid-json.com")

    assert "Expecting value" in str(exc_info.value)
    mock_get.assert_called_once_with("http://api-with-invalid-json.com")
