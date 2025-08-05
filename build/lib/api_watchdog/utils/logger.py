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
    logger = logging.getLogger(name)

    # If logger already exists, check what handlers we need to add
    if logger.handlers:
        has_console_handler = any(
            isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler) 
            for h in logger.handlers
        )
        has_file_handler = any(
            isinstance(h, logging.FileHandler) for h in logger.handlers
        )
        
        # Add console handler if needed
        if log_to_console and not has_console_handler:
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s: %(message)s %(funcName)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
            
        # Add file handler if needed
        if log_to_file and not has_file_handler:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s: %(message)s %(funcName)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
        return logger

    logger.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s %(funcName)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if log_to_console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # File handler
    if log_to_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
