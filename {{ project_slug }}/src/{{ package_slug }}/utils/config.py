"""
Configuration utilities for {{ project_name }}.

This module provides utilities for loading and managing configuration.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

from ..core.system import SystemConfig
from ..core.exceptions import ConfigurationError


def load_config(config_path: Path) -> SystemConfig:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if not isinstance(config_data, dict):
            raise ConfigurationError("Configuration file must contain a dictionary")
        
        # Create system config with default values
        config = SystemConfig()
        
        # Update with values from file
        for key, value in config_data.items():
            if hasattr(config, key):
                setattr(config, key, value)
            else:
                config.additional_settings[key] = value
        
        # Validate the configuration
        config.validate()
        
        return config
        
    except FileNotFoundError:
        raise ConfigurationError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML in configuration file: {e}")
    except Exception as e:
        raise ConfigurationError(f"Error loading configuration: {e}")


def save_config(config: SystemConfig, config_path: Path) -> None:
    """Save configuration to a YAML file."""
    try:
        # Ensure the directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert config to dictionary
        config_dict = config.to_dict()
        
        # Write to file
        with open(config_path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            
    except Exception as e:
        raise ConfigurationError(f"Error saving configuration: {e}")


def load_env_config() -> SystemConfig:
    """Load configuration from environment variables."""
    try:
        return SystemConfig.from_env()
    except Exception as e:
        raise ConfigurationError(f"Error loading environment configuration: {e}")


def merge_configs(base_config: SystemConfig, override_config: Dict[str, Any]) -> SystemConfig:
    """Merge a base configuration with override values."""
    try:
        # Create a copy of the base config
        merged_config = SystemConfig(**base_config.to_dict())
        
        # Apply overrides
        for key, value in override_config.items():
            if hasattr(merged_config, key):
                setattr(merged_config, key, value)
            else:
                merged_config.additional_settings[key] = value
        
        # Validate the merged configuration
        merged_config.validate()
        
        return merged_config
        
    except Exception as e:
        raise ConfigurationError(f"Error merging configurations: {e}")


def get_config_value(config: SystemConfig, key: str, default: Any = None) -> Any:
    """Get a configuration value with a default."""
    return config.get(key, default)


def set_config_value(config: SystemConfig, key: str, value: Any) -> None:
    """Set a configuration value."""
    if hasattr(config, key):
        setattr(config, key, value)
    else:
        config.additional_settings[key] = value


def validate_config_file(config_path: Path) -> bool:
    """Validate a configuration file without loading it."""
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if not isinstance(config_data, dict):
            return False
        
        # Try to create a SystemConfig to validate
        config = SystemConfig()
        for key, value in config_data.items():
            if hasattr(config, key):
                setattr(config, key, value)
            else:
                config.additional_settings[key] = value
        
        config.validate()
        return True
        
    except Exception:
        return False

