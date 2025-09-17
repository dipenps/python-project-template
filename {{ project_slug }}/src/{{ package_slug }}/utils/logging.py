"""
Logging utilities for {{ project_name }}.

This module provides utilities for setting up and managing logging.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    log_format: Optional[str] = None,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """Set up logging configuration."""
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Default log format
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """Set the logging level for all handlers."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    for handler in root_logger.handlers:
        handler.setLevel(numeric_level)


def add_file_handler(
    log_file: Path,
    level: str = "INFO",
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> None:
    """Add a file handler to the root logger."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_file_size,
        backupCount=backup_count
    )
    file_handler.setLevel(numeric_level)
    
    # Use the same formatter as console handler
    root_logger = logging.getLogger()
    if root_logger.handlers:
        formatter = root_logger.handlers[0].formatter
        file_handler.setFormatter(formatter)
    
    root_logger.addHandler(file_handler)


def remove_file_handler(log_file: Path) -> None:
    """Remove a file handler from the root logger."""
    root_logger = logging.getLogger()
    
    # Find and remove the handler for the specified file
    handlers_to_remove = []
    for handler in root_logger.handlers:
        if (isinstance(handler, logging.handlers.RotatingFileHandler) and
            handler.baseFilename == str(log_file.absolute())):
            handlers_to_remove.append(handler)
    
    for handler in handlers_to_remove:
        root_logger.removeHandler(handler)
        handler.close()


def log_exception(logger: logging.Logger, message: str, exc_info: bool = True) -> None:
    """Log an exception with full traceback."""
    logger.error(message, exc_info=exc_info)


def log_performance(logger: logging.Logger, operation: str, duration: float) -> None:
    """Log performance metrics."""
    logger.info(f"Performance: {operation} took {duration:.3f} seconds")


def create_structured_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: str = "INFO"
) -> logging.Logger:
    """Create a logger with structured logging configuration."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Set level
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(numeric_level)
        
        # Create formatter for structured logging
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger

