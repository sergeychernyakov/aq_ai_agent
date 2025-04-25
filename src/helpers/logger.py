# src/helpers/logger.py

"""
Logger utility module.

This module provides a utility function for setting up and retrieving a logger 
with specific configurations such as log level and handlers.
"""

import logging
from src.config import config

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance with a specified configuration.

    This function sets up a logger with both file and stream handlers. It ensures
    that multiple handlers are not added to the same logger to prevent duplicate logs.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Prevent adding multiple handlers to the same logger
        logging.basicConfig(
            level=logging.DEBUG if config.DEBUG else logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(f"tmp/logs/{name}.log"),
                logging.StreamHandler(),
            ],
        )
    return logger
