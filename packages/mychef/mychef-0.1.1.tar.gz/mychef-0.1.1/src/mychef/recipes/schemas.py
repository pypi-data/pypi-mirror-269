from pydantic import AnyUrl

from mychef.core.schemas import BaseSchema


class InIngredientSchema(BaseSchema):
    """Ingredient input from user."""

    name: str


class IngredientSchema(BaseSchema):
    """Ingredient fetched from the persistence layer."""

    id: int
    name: str


class InRecipeSchema(BaseSchema):
    """Recipe input from user."""

    name: str
    url: AnyUrl
    images: list[AnyUrl]
    ingredients: list[str]


class RecipeSchema(BaseSchema):
    """Recipe fetched from the persistence layer."""

    id: int
    name: str
    url: str
    created_by: str
    images: list[str]
    ingredients: list[str]
