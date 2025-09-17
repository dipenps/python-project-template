"""
Core components for {{ project_name }}.

This module contains the fundamental building blocks of the agent-based system.
"""

from .agent import BaseAgent, AgentStatus, AgentConfig, AgentManager
from .exceptions import AgentError, ConfigurationError, CommunicationError, SystemError
from .system import SystemConfig

__all__ = [
    "BaseAgent",
    "AgentStatus", 
    "AgentConfig",
    "AgentManager",
    "AgentError",
    "ConfigurationError",
    "CommunicationError", 
    "SystemError",
    "SystemConfig",
]

