"""CLI commands for shorty."""

import click

from shorty.db import init_db
from shorty.shortener import shorten as _shorten


@click.group()
def cli() -> None:
    """shorty — URL shortener CLI."""


@cli.command()
def init() -> None:
    """Initialize the database."""
    path = init_db()
    click.echo(f"Database initialized at {path}")


@cli.command()
@click.argument("url")
def shorten(url: str) -> None:
    """Shorten a URL and print the short code."""
    try:
        link = _shorten(url)
        click.echo(f"Short code: {link.code}")
        if link.hits > 0:
            click.echo(f"(already stored, {link.hits} hits)")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
