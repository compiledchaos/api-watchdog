"""Configuration for pytest."""
import os
import tempfile
import json
from pathlib import Path
import pytest

from api_watchdog.utils.logger import get_logger


@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file for testing and clean up after."""
    log_file = tmp_path / "test.log"
    yield str(log_file)
    # No need for manual cleanup - tmp_path handles it


@pytest.fixture
def logger_instance(temp_log_file):
    """Provide a configured logger instance for testing."""
    logger = get_logger(
        "test_logger",
        log_to_file=True,
        log_file=temp_log_file,
        log_to_console=False
    )
    yield logger
    
    # Clean up logger handlers to prevent file handle leaks
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


@pytest.fixture
def mock_response():
    """Create a mock response for testing API calls."""
    def _mock_response(json_data, status_code=200, text=None):
        class MockResponse:
            def __init__(self, json_data, status_code, text):
                self.json_data = json_data
                self.status_code = status_code
                self.text = text or json.dumps(json_data)
                
            def json(self):
                return self.json_data
                
            def raise_for_status(self):
                if 400 <= self.status_code < 600:
                    raise requests.HTTPError(f"HTTP Error {self.status_code}")
                    
        return MockResponse(json_data, status_code, text)
    return _mock_response


@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing."""
    return {
        "coord": {"lon": -0.1257, "lat": 51.5085},
        "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
        "base": "stations",
        "main": {
            "temp": 282.55,
            "feels_like": 281.86,
            "temp_min": 280.37,
            "temp_max": 284.26,
            "pressure": 1023,
            "humidity": 100
        },
        "visibility": 10000,
        "wind": {"speed": 1.03, "deg": 0},
        "clouds": {"all": 1},
        "dt": 1624000000,
        "sys": {"type": 1, "id": 1414, "country": "GB", "sunrise": 1623970000, "sunset": 1624030000},
        "timezone": 3600,
        "id": 2643743,
        "name": "London",
        "cod": 200
    }


@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    return {
        "symbol": "AAPL",
        "companyName": "Apple Inc.",
        "latestPrice": 150.00,
        "change": 1.50,
        "changePercent": 1.01,
        "latestUpdate": 1624000000000,
        "previousClose": 148.50,
        "marketCap": 2500000000000,
        "peRatio": 28.5,
        "week52High": 157.26,
        "week52Low": 103.10
    }


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    config_data = {
        "weather_api": {
            "enabled": True,
            "api_key": "test_api_key",
            "location": "London,uk",
            "polling_interval": 300
        },
        "stock_api": {
            "enabled": True,
            "api_key": "test_stock_key",
            "symbols": ["AAPL", "MSFT"],
            "polling_interval": 900
        },
        "logging": {
            "level": "DEBUG",
            "file": "api_watchdog.log"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        config_file = f.name
    
    yield config_file
    
    # Cleanup
    try:
        os.unlink(config_file)
    except OSError:
        pass
