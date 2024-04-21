import asyncio

import click
import pydantic

from mychef.core import exceptions, sessions

from . import services


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def users() -> None:
    """Control panel for managing users."""


@click.command("add")
@click.option(
    "--username",
    type=str,
    prompt="Username",
    help="Username input. [prompt]",
)
@click.option(
    "--password",
    type=str,
    prompt="Password",
    hide_input=True,
    confirmation_prompt=True,
    help="Password input. [prompt]",
)
def add_user(username: str, password: str) -> None:
    """Add new user."""
    try:
        asyncio.run(add_user_(username, password))
    except exceptions.AlreadyExists:
        click.secho("User already exists.", fg="yellow")
    except pydantic.ValidationError as err:
        click.secho(f"Input validation failed: {err}", fg="yellow")
    else:
        click.secho(f"`{username}` successfully added.", fg="green")


async def add_user_(username: str, password: str) -> None:
    async with sessions.async_session() as session:
        access_service = services.AccessService.from_session(session)
        await access_service.register_user(username, password)
        await session.commit()


@click.command("list")
def list_usernames() -> None:
    """List stored usernames."""
    if usernames := asyncio.run(list_usernames_()):
        click.secho("Stored users:", fg="green")
        for username in sorted(usernames):
            click.echo(f"- {username}")
    else:
        click.secho("No users found.", fg="yellow")


async def list_usernames_() -> list[str]:
    async with sessions.async_session() as session:
        access_service = services.AccessService.from_session(session)
        return await access_service.list_usernames()


users.add_command(add_user)
users.add_command(list_usernames)
