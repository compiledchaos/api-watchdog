
import sys
import pytest
from api_watchdog.core_gui_and_cli.cli import parse_args
from api_watchdog.utils.api_configuration import WeatherConfig, StockConfig

def run_parse(argv):
    bak = sys.argv[:]
    try:
        sys.argv = ["prog"] + argv
        return parse_args()
    finally:
        sys.argv = bak

def test_parse_args_weather_ok():
    args = run_parse(["weather","--location","Chennai","--interval","10","--log-file","w.log"])
    d = vars(args)
    assert d.get("api") is WeatherConfig  # parser maps subcommand to config class
    assert d.get("location") == "Chennai"
    assert d.get("interval") == 10
    assert d.get("log_file") == "w.log"
    assert d.get("cli") in (True, False)

def test_parse_args_stock_ok():
    args = run_parse(["stock","--stock","AAPL","--interval","7","--log-file","s.log"])
    d = vars(args)
    assert d.get("api") is StockConfig
    assert d.get("stock") == "AAPL"
    assert d.get("interval") == 7
    assert d.get("log_file") == "s.log"

def test_parse_args_missing_required_raises():
    with pytest.raises(SystemExit):
        run_parse(["weather"])  # missing --location
    with pytest.raises(SystemExit):
        run_parse(["stock"])  # missing --stock
