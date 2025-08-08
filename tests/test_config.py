"""Tests for the configuration module."""
import os
from unittest.mock import patch, MagicMock
import pytest

from api_watchdog.utils.config import WeatherConfig, StockConfig


@patch('api_watchdog.utils.config.load_dotenv')
def test_weather_config_initialization(mock_load_dotenv):
    """Test WeatherConfig class initialization."""
    # Setup
    mock_logger = MagicMock()
    location = "London,uk"
    interval = 300
    log_file = "weather.log"
    
    # Test
    with patch.dict('os.environ', {'OPENWEATHERMAP_API_KEY': 'test_key'}):
        config = WeatherConfig(location, mock_logger, interval, log_file)
    
    # Verify
    expected_url = "https://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=test_key"
    assert config.api_url == expected_url
    assert config.interval == interval
    assert config.log_file == log_file


@patch('api_watchdog.utils.config.load_dotenv')
def test_stock_config_initialization(mock_load_dotenv):
    """Test StockConfig class initialization."""
    # Setup
    mock_logger = MagicMock()
    symbol = "AAPL"
    interval = 5  # minutes
    log_file = "stock.log"
    
    # Test
    with patch.dict('os.environ', {'ALPHAVANTAGE_API_KEY': 'test_key'}):
        config = StockConfig(symbol, mock_logger, interval, log_file)
    
    # Verify
    expected_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=test_key"
    assert config.api_url == expected_url
    assert config.interval == 5  # Should be in minutes for stocks
    assert config.log_file == log_file


def test_weather_config_get_config():
    """Test WeatherConfig get_config method."""
    # Setup
    mock_logger = MagicMock()
    with patch.dict('os.environ', {'OPENWEATHERMAP_API_KEY': 'test_key'}):
        config = WeatherConfig("London,uk", mock_logger, 300, "weather.log")
    
    # Test
    api_url, interval, log_file = config.get_config()
    
    # Verify
    assert "London,uk" in api_url
    assert "test_key" in api_url
    assert interval == 300
    assert log_file == "weather.log"


def test_weather_config_configuration(capsys):
    """Test WeatherConfig configuration method."""
    # Setup
    mock_logger = MagicMock()
    with patch.dict('os.environ', {'OPENWEATHERMAP_API_KEY': 'test_key'}):
        config = WeatherConfig("London,uk", mock_logger, 300, "weather.log")
    
    # Test data
    test_data = {
        "name": "London",
        "dt": 1624000000,
        "sys": {"country": "GB", "sunrise": 1623970000, "sunset": 1624030000},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 5.5, "deg": 180},
        "main": {"temp": 288.15, "humidity": 70, "pressure": 1013},
        "visibility": 10000,
        "clouds": {"all": 20}
    }
    
    # Test
    config.configuration(test_data)
    
    # Verify log calls
    expected_logs = [
        "Location: London",
        "Country: GB",
        "Weather: clear sky"
    ]
    
    # Check that all expected logs were made
    for log in expected_logs:
        mock_logger.info.assert_any_call(log)


def test_stock_config_get_config():
    """Test StockConfig get_config method."""
    # Setup
    mock_logger = MagicMock()
    with patch.dict('os.environ', {'ALPHAVANTAGE_API_KEY': 'test_key'}):
        config = StockConfig("AAPL", mock_logger, 5, "stock.log")
    
    # Test
    api_url, interval, log_file = config.get_config()
    
    # Verify
    assert "AAPL" in api_url
    assert "test_key" in api_url
    assert interval == 5
    assert log_file == "stock.log"


def test_stock_config_configuration(capsys):
    """Test StockConfig configuration method."""
    # Setup
    mock_logger = MagicMock()
    with patch.dict('os.environ', {'ALPHAVANTAGE_API_KEY': 'test_key'}):
        config = StockConfig("AAPL", mock_logger, 5, "stock.log")
    
    # Test data - simplified for testing
    test_data = {
        "Meta Data": {
            "1. Information": "Intraday (5min) open, high, low, close prices and volume",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2023-06-15 19:55:00"
        },
        "Time Series (5min)": {
            "2023-06-15 19:55:00": {
                "1. open": "185.5000",
                "2. high": "185.8000",
                "3. low": "185.4500",
                "4. close": "185.7000",
                "5. volume": "123456"
            }
        }
    }
    
    # Test
    config.configuration(test_data)
    
    # Verify log calls
    expected_logs = [
        "Stock: AAPL",
        "Time: 2023-06-15 19:55:00",
        "Open: 185.5000",
        "High: 185.8000",
        "Low: 185.4500",
        "Close: 185.7000",
        "Volume: 123456"
    ]
    
    # Check that all expected logs were made
    for log in expected_logs:
        mock_logger.info.assert_any_call(log)
