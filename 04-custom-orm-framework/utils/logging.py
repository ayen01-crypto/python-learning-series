"""
Logging Utilities
This module provides logging functionality for the ORM framework.
"""

import logging
import sys
from typing import Optional
from config import config


def setup_logger(name: str = "orm", level: Optional[str] = None) -> logging.Logger:
    """Set up and return a logger."""
    if level is None:
        level = config.LOG_LEVEL
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent adding multiple handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if config.LOG_FILE:
        file_handler = logging.FileHandler(config.LOG_FILE)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "orm") -> logging.Logger:
    """Get a logger instance."""
    return setup_logger(name)


# Global logger instance
logger = get_logger()