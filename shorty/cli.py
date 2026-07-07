"""CLI commands for shorty."""

import click

from shorty.db import init_db
from shorty.shortener import shorten as _shorten
from shorty.shortener import resolve as _resolve
from shorty.shortener import list_links, delete_link


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


@cli.command()
@click.argument("code")
def resolve(code: str) -> None:
    """Resolve a short code to its original URL."""
    try:
        link = _resolve(code)
        click.echo(link.url)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command("list")
def list_cmd() -> None:
    """List all stored links."""
    links = list_links()
    if not links:
        click.echo("No links stored.")
        return
    for link in links:
        click.echo(f"{link.code}  {link.url}  ({link.hits} hits)")


@cli.command()
@click.argument("code")
def delete(code: str) -> None:
    """Delete a stored link by short code."""
    try:
        delete_link(code)
        click.echo(f"Deleted: {code}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
