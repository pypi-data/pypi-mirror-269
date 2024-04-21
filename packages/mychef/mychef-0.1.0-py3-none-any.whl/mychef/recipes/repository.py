from collections.abc import Iterable
from typing import Protocol

import sqlalchemy.exc
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from mychef.core import exceptions

from . import schemas, tables


class SupportsIngredientRepository(Protocol):
    async def create(
        self, ingredient: schemas.InIngredientSchema
    ) -> schemas.IngredientSchema:
        """Create ingredient after validating input schema."""
        ...

    async def get_all(self) -> list[schemas.IngredientSchema]:
        """Fetch all ingredients from from DB."""
        ...

    async def bulk_create(self, ingredients: Iterable[str]) -> None:
        """Create or ignore ingredients in bulk."""
        ...


class SqlalchemyIngredientRepository:
    """Implement the ingredient repository with sqlite."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, ingredient: schemas.InIngredientSchema
    ) -> schemas.IngredientSchema:
        entry = tables.Ingredient(**ingredient.model_dump())
        self._session.add(entry)
        try:
            await self._session.commit()
            return schemas.IngredientSchema.model_validate(entry)
        except sqlalchemy.exc.IntegrityError as err:
            await self._session.rollback()
            raise exceptions.AlreadyExists(err) from err

    async def get_all(self) -> list[schemas.IngredientSchema]:
        results = await self._session.execute(select(tables.Ingredient))
        return [
            schemas.IngredientSchema.model_validate(result)
            for result in results.scalars()
        ]

    async def bulk_create(self, ingredients: Iterable[str]) -> None:
        for ingredient in ingredients:
            try:
                await self.create(schemas.InIngredientSchema(name=ingredient))
            except exceptions.AlreadyExists:
                continue


class SupportsRecipeRepository(Protocol):
    async def create(
        self, recipe: schemas.InRecipeSchema, created_by: str
    ) -> schemas.RecipeSchema:
        """Create recipe after validating input schema."""
        ...

    async def get_all(self) -> list[schemas.RecipeSchema]:
        """Fetch all recipes from from DB."""
        ...

    async def get_by_ingredients(
        self,
        ingredients: Iterable[str],
        must_include_all: bool = False,
        absolute_match: bool = False,
    ) -> list[schemas.RecipeSchema]:
        """Get recipes based on provided ingredients."""
        ...


class SqlalchemyRecipeRepository:
    """Implement the recipe repository with sqlite."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, recipe: schemas.InRecipeSchema, created_by: str
    ) -> schemas.RecipeSchema:
        entry = tables.Recipe(
            **recipe.model_dump(exclude={"url", "images"}),
            created_by=created_by,
            url=str(recipe.url),
            images=[str(image) for image in recipe.images],
        )
        self._session.add(entry)
        try:
            await self._session.commit()
            return schemas.RecipeSchema.model_validate(entry)
        except sqlalchemy.exc.IntegrityError as err:
            await self._session.rollback()
            raise exceptions.AlreadyExists(err) from err

    async def get_all(self) -> list[schemas.RecipeSchema]:
        results = await self._session.execute(select(tables.Recipe))
        return [
            schemas.RecipeSchema.model_validate(result) for result in results.scalars()
        ]

    async def get_by_ingredients(
        self,
        ingredients: Iterable[str],
        must_include_all: bool = False,
        absolute_match: bool = False,
    ) -> list[schemas.RecipeSchema]:
        if absolute_match:
            ingredients = (f'"{item}"' for item in ingredients)

        conditional = and_ if must_include_all else or_
        conditions = [tables.Recipe.ingredients.contains(item) for item in ingredients]
        qry = select(tables.Recipe).filter(conditional(*conditions))
        results = await self._session.execute(qry)
        return [
            schemas.RecipeSchema.model_validate(result) for result in results.scalars()
        ]
