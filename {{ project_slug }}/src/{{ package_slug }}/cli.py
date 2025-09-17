"""
Command-line interface for {{ project_name }}.

This module provides the main CLI entry point and command handling.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

import click
import yaml

from .core import AgentManager, SystemConfig
from .utils.logging import setup_logging
from .utils.config import load_config


@click.group()
@click.option(
    "--config", 
    "-c", 
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file"
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the logging level"
)
@click.option(
    "--verbose", 
    "-v", 
    is_flag=True, 
    help="Enable verbose output"
)
@click.pass_context
def cli(ctx: click.Context, config: Optional[Path], log_level: str, verbose: bool) -> None:
    """{{ project_name }} - A Python project with agent-based architecture."""
    # Set up logging
    if verbose:
        log_level = "DEBUG"
    
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    try:
        if config:
            cfg = load_config(config)
        else:
            cfg = SystemConfig()
        ctx.obj["config"] = cfg
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--host",
    default="localhost",
    help="Host to bind the server to"
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port to bind the server to"
)
@click.option(
    "--workers",
    default=1,
    type=int,
    help="Number of worker processes"
)
@click.pass_context
def run(ctx: click.Context, host: str, port: int, workers: int) -> None:
    """Run the agent system."""
    config = ctx.obj["config"]
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting {{ project_name }} on {host}:{port}")
    logger.info(f"Using {workers} worker(s)")
    
    try:
        # Create and start agent manager
        manager = AgentManager(config)
        asyncio.run(manager.start())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error starting system: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--agent-id",
    required=True,
    help="ID of the agent to check"
)
@click.pass_context
def status(ctx: click.Context, agent_id: str) -> None:
    """Check the status of a specific agent."""
    config = ctx.obj["config"]
    logger = logging.getLogger(__name__)
    
    try:
        # This would typically connect to a running system
        # For now, just show a placeholder message
        click.echo(f"Agent {agent_id} status: Not implemented yet")
        logger.info(f"Checking status for agent: {agent_id}")
    except Exception as e:
        logger.error(f"Error checking agent status: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Output file for configuration"
)
@click.pass_context
def config(ctx: click.Context, output: Optional[Path]) -> None:
    """Manage system configuration."""
    config = ctx.obj["config"]
    logger = logging.getLogger(__name__)
    
    try:
        if output:
            # Save current configuration to file
            with open(output, 'w') as f:
                yaml.dump(config.__dict__, f, default_flow_style=False)
            click.echo(f"Configuration saved to {output}")
        else:
            # Display current configuration
            click.echo("Current configuration:")
            click.echo(yaml.dump(config.__dict__, default_flow_style=False))
        
        logger.info("Configuration operation completed")
    except Exception as e:
        logger.error(f"Error managing configuration: {e}")
        sys.exit(1)


@cli.command()
def version() -> None:
    """Show version information."""
    from . import __version__, __author__, __email__
    
    click.echo(f"{{ project_name }} version {__version__}")
    click.echo(f"Author: {__author__} <{__email__}>")
    click.echo(f"Python version: {sys.version}")


def main() -> None:
    """Main entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()

