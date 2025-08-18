
import pytest
from unittest.mock import patch, Mock
from api_watchdog.utils.api_fetcher import fetch_api
import requests

def test_fetch_api_success_json():
    mock_resp = Mock()
    mock_resp.raise_for_status = Mock()
    mock_resp.json.return_value = {"ok": True}
    with patch("api_watchdog.utils.api_fetcher.requests.get", return_value=mock_resp) as mget:
        data = fetch_api("https://example.com/data", max_retries=3, delay=0)
        assert data == {"ok": True}
        assert mget.call_count == 1
        mget.assert_called_with("https://example.com/data", timeout=10)

def test_fetch_api_http_error_retries_and_raises():
    mock_resp = Mock()
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("boom")
    with patch("api_watchdog.utils.api_fetcher.requests.get", return_value=mock_resp) as mget:
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_api("https://example.com/err", max_retries=3, delay=0)
        # Should have attempted exactly max_retries times
        assert mget.call_count == 3

def test_fetch_api_timeout_retries_and_raises():
    # Simulate a RequestException such as Timeout on get()
    with patch("api_watchdog.utils.api_fetcher.requests.get", side_effect=requests.exceptions.Timeout("t")) as mget:
        with pytest.raises(requests.exceptions.Timeout):
            fetch_api("https://example.com/timeout", max_retries=2, delay=0)
        assert mget.call_count == 2

def test_fetch_api_non_json_bubbles_value_error():
    mock_resp = Mock()
    mock_resp.raise_for_status = Mock()
    mock_resp.json.side_effect = ValueError("not json")
    with patch("api_watchdog.utils.api_fetcher.requests.get", return_value=mock_resp):
        with pytest.raises(ValueError):
            fetch_api("https://example.com/notjson", max_retries=1, delay=0)
