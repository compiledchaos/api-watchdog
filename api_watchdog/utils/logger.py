import logging
from pathlib import Path


def get_logger(
    name: str = "api_watchdog",
    log_to_file: bool = True,
    log_file: str = "api_watchdog.log",
    log_to_console: bool = False,
) -> logging.Logger:
    """
    Returns a logger instance with the specified name and configuration.

    Args:
        name: The name of the logger.
        log_to_file: The logger will write logs to a file.
        log_file: The path to the log file.
        log_to_console: The logger will write logs to the console.

    The function returns a logger instance with the specified name and configuration.
    If the logger already exists, it returns the existing logger instance. Otherwise,
    it creates a new logger instance with the specified name and configuration.
    """

    # Obtain a logger instance with the specified name
    logger = logging.getLogger(name)

    # Check if the logger already has handlers
    if logger.handlers:
        # Determine if a console handler is already present
        has_console_handler = any(
            isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
            for h in logger.handlers
        )
        # Determine if a file handler is already present
        has_file_handler = any(
            isinstance(h, logging.FileHandler) for h in logger.handlers
        )

        # Add a console handler if logging to console is enabled and no handler is present
        if log_to_console and not has_console_handler:
            # Define the format for the console log messages
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            # Create and configure the console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        # Add a file handler if logging to file is enabled and no handler is present
        if log_to_file and not has_file_handler:
            # Ensure that the directory for the log file exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            # Create and configure the file handler
            fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        # Return the logger instance with updated handlers
        return logger

    # Set the default logging level for the logger
    logger.setLevel(logging.INFO)

    # Define a formatter for log messages
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Add a console handler if logging to console is enabled
    if log_to_console:
        # Create and configure the console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # Add a file handler if logging to file is enabled
    if log_to_file:
        # Ensure that the directory for the log file exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        # Create and configure the file handler
        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # Return the fully configured logger instance
    return logger
