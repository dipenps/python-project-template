"""
Logging configuration for the project.
"""
import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    """
    Set up basic logging.

    Args:
        level: The logging level to use.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
