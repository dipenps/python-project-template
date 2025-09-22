"""
Core settings and configuration for the project.

This module uses Pydantic for robust and type-safe settings management.
Settings can be loaded from environment variables or a .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines the application's settings.

    These settings are automatically loaded from environment variables.
    For example, the `LOG_LEVEL` setting will be populated by the
    `LOG_LEVEL` environment variable.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "{{ project_name }}"
    LOG_LEVEL: str = "INFO"


# Create a singleton instance of the settings
settings = Settings()

