"""CLI commands for shorty."""

import click

from shorty.db import init_db


@click.group()
def cli() -> None:
    """shorty — URL shortener CLI."""


@cli.command()
def init() -> None:
    """Initialize the database."""
    path = init_db()
    click.echo(f"Database initialized at {path}")


if __name__ == "__main__":
    cli()
