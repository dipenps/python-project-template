"""
Validation utilities for {{ project_name }}.

This module provides utilities for validating data and configurations.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..core.exceptions import ValidationError


def validate_agent_message(message: Dict[str, Any]) -> bool:
    """Validate an agent message."""
    try:
        # Check required fields
        required_fields = ["id", "type", "sender", "recipient", "timestamp", "payload"]
        for field in required_fields:
            if field not in message:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate message ID
        if not isinstance(message["id"], str) or not message["id"].strip():
            raise ValidationError("Message ID must be a non-empty string")
        
        # Validate message type
        valid_types = ["command", "event", "query", "response", "error", "heartbeat"]
        if message["type"] not in valid_types:
            raise ValidationError(f"Invalid message type: {message['type']}")
        
        # Validate sender and recipient
        if not isinstance(message["sender"], str) or not message["sender"].strip():
            raise ValidationError("Sender must be a non-empty string")
        
        if not isinstance(message["recipient"], str) or not message["recipient"].strip():
            raise ValidationError("Recipient must be a non-empty string")
        
        # Validate timestamp
        if not isinstance(message["timestamp"], str):
            raise ValidationError("Timestamp must be a string")
        
        try:
            datetime.fromisoformat(message["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            raise ValidationError("Invalid timestamp format")
        
        # Validate payload
        if not isinstance(message["payload"], dict):
            raise ValidationError("Payload must be a dictionary")
        
        return True
        
    except ValidationError:
        return False
    except Exception:
        return False


def validate_agent_config(config: Dict[str, Any]) -> bool:
    """Validate agent configuration."""
    try:
        # Check required fields
        required_fields = ["agent_id", "agent_type", "settings", "dependencies", "resources"]
        for field in required_fields:
            if field not in config:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate agent ID
        if not isinstance(config["agent_id"], str) or not config["agent_id"].strip():
            raise ValidationError("Agent ID must be a non-empty string")
        
        # Validate agent ID format (alphanumeric, underscore, hyphen)
        if not re.match(r'^[a-zA-Z0-9_-]+$', config["agent_id"]):
            raise ValidationError("Agent ID must contain only alphanumeric characters, underscores, and hyphens")
        
        # Validate agent type
        if not isinstance(config["agent_type"], str) or not config["agent_type"].strip():
            raise ValidationError("Agent type must be a non-empty string")
        
        # Validate settings
        if not isinstance(config["settings"], dict):
            raise ValidationError("Settings must be a dictionary")
        
        # Validate dependencies
        if not isinstance(config["dependencies"], list):
            raise ValidationError("Dependencies must be a list")
        
        for dep in config["dependencies"]:
            if not isinstance(dep, str) or not dep.strip():
                raise ValidationError("Each dependency must be a non-empty string")
        
        # Validate resources
        if not isinstance(config["resources"], dict):
            raise ValidationError("Resources must be a dictionary")
        
        resource_fields = ["max_memory", "max_cpu", "max_connections", "max_processing_time"]
        for field in resource_fields:
            if field not in config["resources"]:
                raise ValidationError(f"Missing required resource field: {field}")
        
        # Validate resource values
        if not isinstance(config["resources"]["max_memory"], int) or config["resources"]["max_memory"] <= 0:
            raise ValidationError("max_memory must be a positive integer")
        
        if not isinstance(config["resources"]["max_cpu"], (int, float)) or config["resources"]["max_cpu"] <= 0:
            raise ValidationError("max_cpu must be a positive number")
        
        if not isinstance(config["resources"]["max_connections"], int) or config["resources"]["max_connections"] <= 0:
            raise ValidationError("max_connections must be a positive integer")
        
        if not isinstance(config["resources"]["max_processing_time"], (int, float)) or config["resources"]["max_processing_time"] <= 0:
            raise ValidationError("max_processing_time must be a positive number")
        
        return True
        
    except ValidationError:
        return False
    except Exception:
        return False


def validate_string(value: Any, field_name: str, min_length: int = 1, max_length: Optional[int] = None) -> str:
    """Validate a string value."""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")
    
    if len(value.strip()) < min_length:
        raise ValidationError(f"{field_name} must be at least {min_length} characters long")
    
    if max_length is not None and len(value) > max_length:
        raise ValidationError(f"{field_name} must be no more than {max_length} characters long")
    
    return value.strip()


def validate_integer(value: Any, field_name: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    """Validate an integer value."""
    if not isinstance(value, int):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be an integer")
    
    if min_value is not None and value < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}")
    
    if max_value is not None and value > max_value:
        raise ValidationError(f"{field_name} must be no more than {max_value}")
    
    return value


def validate_float(value: Any, field_name: str, min_value: Optional[float] = None, max_value: Optional[float] = None) -> float:
    """Validate a float value."""
    if not isinstance(value, (int, float)):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a number")
    
    if min_value is not None and value < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}")
    
    if max_value is not None and value > max_value:
        raise ValidationError(f"{field_name} must be no more than {max_value}")
    
    return value


def validate_list(value: Any, field_name: str, item_type: type = str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> List[Any]:
    """Validate a list value."""
    if not isinstance(value, list):
        raise ValidationError(f"{field_name} must be a list")
    
    if min_length is not None and len(value) < min_length:
        raise ValidationError(f"{field_name} must have at least {min_length} items")
    
    if max_length is not None and len(value) > max_length:
        raise ValidationError(f"{field_name} must have no more than {max_length} items")
    
    for i, item in enumerate(value):
        if not isinstance(item, item_type):
            raise ValidationError(f"{field_name}[{i}] must be of type {item_type.__name__}")
    
    return value


def validate_dict(value: Any, field_name: str, required_keys: Optional[List[str]] = None, optional_keys: Optional[List[str]] = None) -> Dict[str, Any]:
    """Validate a dictionary value."""
    if not isinstance(value, dict):
        raise ValidationError(f"{field_name} must be a dictionary")
    
    if required_keys:
        for key in required_keys:
            if key not in value:
                raise ValidationError(f"{field_name} must contain required key: {key}")
    
    if optional_keys:
        for key in value.keys():
            if key not in required_keys and key not in optional_keys:
                raise ValidationError(f"{field_name} contains unexpected key: {key}")
    
    return value


def validate_email(email: str) -> str:
    """Validate an email address."""
    email = validate_string(email, "email")
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")
    
    return email


def validate_url(url: str) -> str:
    """Validate a URL."""
    url = validate_string(url, "url")
    
    # Basic URL regex pattern
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    if not re.match(pattern, url):
        raise ValidationError("Invalid URL format")
    
    return url

