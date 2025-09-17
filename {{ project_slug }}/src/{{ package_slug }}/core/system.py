"""
System configuration and management for {{ project_name }}.

This module contains system-wide configuration and management functionality.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional


@dataclass
class SystemConfig:
    """System-wide configuration."""
    log_level: str = "INFO"
    max_agents: int = 100
    message_timeout: float = 30.0
    heartbeat_interval: float = 10.0
    cleanup_interval: float = 300.0
    data_dir: str = "./data"
    log_dir: str = "./logs"
    debug: bool = False
    
    # Additional configuration can be added here
    additional_settings: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Post-initialization processing."""
        # Convert string paths to Path objects for easier manipulation
        self.data_dir = str(Path(self.data_dir).resolve())
        self.log_dir = str(Path(self.log_dir).resolve())
        
        # Ensure directories exist
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_env(cls) -> "SystemConfig":
        """Create configuration from environment variables."""
        return cls(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_agents=int(os.getenv("MAX_AGENTS", "100")),
            message_timeout=float(os.getenv("MESSAGE_TIMEOUT", "30.0")),
            heartbeat_interval=float(os.getenv("HEARTBEAT_INTERVAL", "10.0")),
            cleanup_interval=float(os.getenv("CLEANUP_INTERVAL", "300.0")),
            data_dir=os.getenv("DATA_DIR", "./data"),
            log_dir=os.getenv("LOG_DIR", "./logs"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "log_level": self.log_level,
            "max_agents": self.max_agents,
            "message_timeout": self.message_timeout,
            "heartbeat_interval": self.heartbeat_interval,
            "cleanup_interval": self.cleanup_interval,
            "data_dir": self.data_dir,
            "log_dir": self.log_dir,
            "debug": self.debug,
            "additional_settings": self.additional_settings,
        }
    
    def update(self, **kwargs: Any) -> None:
        """Update configuration with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.additional_settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        if hasattr(self, key):
            return getattr(self, key)
        return self.additional_settings.get(key, default)
    
    def validate(self) -> None:
        """Validate the configuration."""
        if self.max_agents <= 0:
            raise ValueError("max_agents must be positive")
        
        if self.message_timeout <= 0:
            raise ValueError("message_timeout must be positive")
        
        if self.heartbeat_interval <= 0:
            raise ValueError("heartbeat_interval must be positive")
        
        if self.cleanup_interval <= 0:
            raise ValueError("cleanup_interval must be positive")
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"log_level must be one of {valid_log_levels}")
        
        # Ensure directories are writable
        data_path = Path(self.data_dir)
        if not data_path.exists():
            data_path.mkdir(parents=True, exist_ok=True)
        
        if not os.access(data_path, os.W_OK):
            raise ValueError(f"data_dir {self.data_dir} is not writable")
        
        log_path = Path(self.log_dir)
        if not log_path.exists():
            log_path.mkdir(parents=True, exist_ok=True)
        
        if not os.access(log_path, os.W_OK):
            raise ValueError(f"log_dir {self.log_dir} is not writable")

