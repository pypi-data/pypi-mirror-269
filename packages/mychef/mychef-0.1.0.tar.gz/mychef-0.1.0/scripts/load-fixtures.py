import asyncio
import logging

from pydantic_core import Url

import mychef.access.repository
import mychef.access.schemas
import mychef.access.services
import mychef.recipes.schemas
import mychef.recipes.services
from mychef.core import exceptions, sessions


async def load_fixtures():
    """Load test fixtures useful for local development."""
    async with sessions.async_session() as session:
        access_svc = mychef.access.services.AccessService.from_session(session)
        recipe_svc = mychef.recipes.services.RecipeService.from_session(session)

        await add_dummy_user(access_svc)
        await add_dummy_recipes(recipe_svc)


async def add_dummy_user(access_svc: mychef.access.services.AccessService):
    try:
        await access_svc.register_user(username="dummy", password="password")
    except exceptions.AlreadyExists:
        logging.info("'dummy' user already exists with password equal to 'password'.")
    else:
        logging.info("Added 'dummy' user with password equal to 'password'.")


async def add_dummy_recipes(recipe_svc: mychef.recipes.services.RecipeService):
    async def add_recipe(name: str, ingredients: list[str]):
        name_slug = "-".join(word.lower() for word in name.split())
        payload = mychef.recipes.schemas.InRecipeSchema(
            name=name,
            url=Url(f"https://recipes.com/{name_slug}"),
            images=[Url(f"https://images.com/{name_slug}")],
            ingredients=ingredients,
        )
        await recipe_svc.register_recipe(payload=payload, username="dummy")

    await add_recipe("Apple Pie", ["apples", "cinnamon"])
    await add_recipe("Pizza", ["tomatoes", "mozarella"])
    await add_recipe("Burrito", ["rice", "tortilla", "sour cream"])

    logging.info("Added example dummy recipes.")


if __name__ == "__main__":
    asyncio.run(load_fixtures())
