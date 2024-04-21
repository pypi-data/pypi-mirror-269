from __future__ import annotations

import dataclasses

from sqlalchemy.ext.asyncio import AsyncSession

from . import repository, schemas


@dataclasses.dataclass(frozen=True)
class RecipeService:
    """The service layer for the recipe domain."""

    _recipe_repo: repository.SupportsRecipeRepository
    _ingred_repo: repository.SupportsIngredientRepository

    @classmethod
    def from_session(cls, session: AsyncSession) -> RecipeService:
        """Build recipe service from database session."""
        return cls(
            _recipe_repo=repository.SqlalchemyRecipeRepository(session),
            _ingred_repo=repository.SqlalchemyIngredientRepository(session),
        )

    async def register_recipe(
        self, payload: schemas.InRecipeSchema, username: str
    ) -> schemas.RecipeSchema:
        """Register raw recipe and its respective ingredients into the system."""
        recipe = await self._recipe_repo.create(payload, username)
        await self._ingred_repo.bulk_create(payload.ingredients)
        return recipe

    async def get_recipes(self) -> list[schemas.RecipeSchema]:
        """Get all recipes."""
        return await self._recipe_repo.get_all()
