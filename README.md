# 📡 API Watchdog

A powerful Python tool that monitors public APIs (like weather, stocks) with both CLI and GUI interfaces. Track changes, get notified, and analyze API responses over time.

## ✨ Features

- **Dual Interface**: Choose between CLI for automation or GUI for visual monitoring
- **Multiple API Support**: Built-in support for weather and stock market data
- **Real-time Monitoring**: Continuously track API endpoints at configurable intervals
- **Comprehensive Logging**: Detailed logs with timestamps for all API interactions
- **Response Comparison**: Automatically detect and highlight changes in API responses
- **Customizable**: Easily configure API endpoints and monitoring parameters

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/compiledchaos/api-watchdog.git
   cd api-watchdog
   ```

2. Install with pip (editable mode for development):
   ```bash
   pip install -e .
   ```

## 🖥️ Usage

### Command Line Interface (CLI)

```bash
# Monitor stock data
api-watchdog stock --stock "IBM" --log-file "stock.log"

# Monitor weather data
api-watchdog weather --city "New York" --log-file "weather.log"
```

### Graphical User Interface (GUI)

```bash
# Launch the GUI
api-watchdog-gui
```

## 🏗️ Project Structure

```
api_watchdog/
├── cli.py           # Command-line interface
├── entry.py         # Main entry point
├── gui.py           # Graphical user interface
└── utils/
    ├── api_fetcher.py  # API interaction logic
    ├── config.py    # Configuration management
    ├── gui_utils.py # GUI helper functions
    └── logger.py    # Logging utilities
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.