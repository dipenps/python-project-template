"""
{{ project_name }} - A Python project with agent-based architecture.

This package provides a framework for building agent-based systems using modern Python tooling.
"""

__version__ = "0.1.0"
__author__ = "{{ author_name }}"
__email__ = "{{ author_email }}"

# Import main components for easy access
from .cli import main as cli_main
from .core import BaseAgent, AgentStatus, AgentConfig
from .agents.protocols import AgentProtocol, MessageType, AgentMessage

__all__ = [
    "cli_main",
    "BaseAgent",
    "AgentStatus", 
    "AgentConfig",
    "AgentProtocol",
    "MessageType",
    "AgentMessage",
]

