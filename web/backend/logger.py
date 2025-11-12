"""
Logging Configuration for Guindo Backend
Centralized logging with proper formatting and levels
"""

import logging
import sys
from datetime import datetime
from typing import Optional

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logger
logger = logging.getLogger("guindo")

# Set default log level
log_level = logging.INFO
if sys.argv and "--debug" in sys.argv:
    log_level = logging.DEBUG

logger.setLevel(log_level)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(log_level)

# Create formatter
formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

# Prevent duplicate logs
logger.propagate = False


def log_request(method: str, path: str, status_code: int, duration_ms: Optional[float] = None):
    """Log HTTP request with details"""
    message = f"{method} {path} - {status_code}"
    if duration_ms is not None:
        message += f" ({duration_ms:.2f}ms)"

    if status_code >= 500:
        logger.error(message)
    elif status_code >= 400:
        logger.warning(message)
    else:
        logger.info(message)


def log_ai_request(analysis_type: str, model: str, tokens: Optional[int] = None):
    """Log AI API request"""
    message = f"AI Request - Type: {analysis_type}, Model: {model}"
    if tokens:
        message += f", Tokens: {tokens}"
    logger.info(message)


def log_error(error: Exception, context: Optional[str] = None):
    """Log error with context"""
    message = f"Error: {str(error)}"
    if context:
        message = f"{context} - {message}"
    logger.error(message, exc_info=True)


# Export logger and helper functions
__all__ = ["logger", "log_request", "log_ai_request", "log_error"]
