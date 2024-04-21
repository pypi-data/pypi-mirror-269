from fastapi import APIRouter, status

from mychef import dependencies
from mychef.core import exceptions, http_exceptions

from . import schemas

router = APIRouter(tags=["recipes"])


@router.post(
    "/recipes",
    status_code=status.HTTP_201_CREATED,
    summary="Creates recipe when passed valid input.",
)
async def handle_create_recipe(
    payload: schemas.InRecipeSchema,
    username: dependencies.UsernameFromBearerToken,
    recipe_service: dependencies.RecipeService,
) -> schemas.RecipeSchema:
    """Defines endpoint for creating recipes."""
    try:
        return await recipe_service.register_recipe(payload, username)
    except exceptions.AlreadyExists:
        detail = f"Recipe already exists with url={payload.url!r}"
        raise http_exceptions.EntityAlreadyExists(detail) from None


@router.get("/recipes", summary="Get all recipes.")
async def handle_get_posts(
    recipe_service: dependencies.RecipeService,
) -> list[schemas.RecipeSchema]:
    """Defines endpoint for retrieving all recipes."""
    return await recipe_service.get_recipes()
