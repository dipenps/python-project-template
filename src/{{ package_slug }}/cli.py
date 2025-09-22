"""
Command-line interface for the project.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

import click
import pandas as pd

from .utils.logging import setup_logging


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the logging level.",
)
@click.pass_context
def cli(ctx: click.Context, log_level: str) -> None:
    """
    A CLI for data processing pipelines.
    """
    setup_logging(log_level)
    ctx.obj = {}


@cli.command()
@click.argument("filepath", type=click.Path(exists=True, path_type=Path))
@click.option("--head", default=5, help="Number of rows to display from the start of the file.")
def process(filepath: Path, head: int) -> None:
    """
    Process a data file and display summary information.

    Reads a CSV file from FILEPATH, prints its dimensions, and shows the
    first N rows.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Processing file: {filepath}")

    try:
        df = pd.read_csv(filepath)
        click.echo(f"Successfully loaded {filepath}")
        click.echo(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        click.echo("\\nFirst {head} rows:")
        click.echo(df.head(head))
    except Exception as e:
        logger.error(f"Failed to process file: {e}")
        click.echo(f"Error: Could not process file '{filepath}'. See logs for details.", err=True)
        sys.exit(1)


@cli.command()
def version() -> None:
    """Show version information."""
    # This dynamic import helps avoid circular dependencies
    # and keeps the version in one place.
    from . import __version__

    click.echo(f"{{ project_name }} version {__version__}")
    click.echo(f"Python version: {sys.version}")


def main() -> None:
    """Main entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()

