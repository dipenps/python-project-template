"""
Custom exceptions for {{ project_name }}.

This module defines the exception hierarchy used throughout the system.
"""


class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass


class ConfigurationError(AgentError):
    """Raised when there is a configuration error."""
    pass


class CommunicationError(AgentError):
    """Raised when there is a communication error between agents."""
    pass


class SystemError(AgentError):
    """Raised when there is a system-level error."""
    pass


class ValidationError(AgentError):
    """Raised when data validation fails."""
    pass


class TimeoutError(AgentError):
    """Raised when an operation times out."""
    pass


class ResourceError(AgentError):
    """Raised when resource limits are exceeded."""
    pass


class AuthenticationError(AgentError):
    """Raised when authentication fails."""
    pass


class AuthorizationError(AgentError):
    """Raised when authorization fails."""
    pass

