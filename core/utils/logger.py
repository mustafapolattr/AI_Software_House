import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a structured logger instance.

    Args:
        name (str): The name of the module calling the logger (usually __name__).
    """
    logger = logging.getLogger(name)

    # If the logger already has handlers, it means it was already configured.
    # We return it immediately to avoid duplicate log messages.
    if logger.hasHandlers():
        return logger

    # --- Configuration ---
    logger.setLevel(logging.INFO)  # Default level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    # Create a handler that writes to STDOUT (Console)
    handler = logging.StreamHandler(sys.stdout)

    # Define a professional format: [Time] [Level] [LoggerName]: Message
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger