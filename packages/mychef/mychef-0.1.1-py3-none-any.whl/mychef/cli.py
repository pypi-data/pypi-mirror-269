import click
import uvicorn
import uvicorn.config

from mychef.__about__ import __version__
from mychef.access.cli import users
from mychef.core import config, hashing
from mychef.migrations.upgrade import upgrade_to_head


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="mychef")
def mychef() -> None:
    """Control panel for managing mychef application."""


@click.command()
def init() -> None:
    """Instantiate the application environment and secret key."""
    click.secho("Secret key for application:", fg="green")

    if config.settings.secret_key:
        click.echo("Key already found in your environment: `SECRET_KEY`\n")
    else:
        click.echo(f"SECRET_KEY={hashing.generate_secret_token()}")
        click.secho("Copy and paste this into your `.env` file.\n", fg="yellow")

    click.secho("Migrating database to head:", fg="green")
    upgrade_to_head()
    click.echo("Successfully migrated to head.")


@click.command()
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Bind socket to this host.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Bind socket to this port.",
    show_default=True,
)
def run(host: str, port: int) -> None:
    """Migrate database to latest version and launch application server."""

    click.secho("Migrating database to head:", fg="green")
    upgrade_to_head()
    click.echo("Successfully migrated to head.\n")

    click.secho("Starting server...", fg="green")
    uvicorn.run(
        "mychef.app:app",
        host=host,
        port=port,
        log_level=config.settings.log_level,
    )


mychef.add_command(init)
mychef.add_command(run)
mychef.add_command(users)
