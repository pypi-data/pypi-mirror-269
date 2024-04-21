import pytest
from pydantic import AnyUrl
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from mychef.recipes import schemas, services


@pytest.fixture
def payload() -> schemas.InRecipeSchema:
    return schemas.InRecipeSchema(
        name="Burrito",
        ingredients=["beans", "rice", "tortilla"],
        url=AnyUrl("http://polloslocos.com/1"),
        images=[AnyUrl("http://polloslocos.com/images/1")],
    )


@pytest.fixture
def recipe_service(db_session: AsyncSession) -> services.RecipeService:
    return services.RecipeService.from_session(db_session)


async def test_recipe_successfully_registered(
    recipe_service: services.RecipeService, payload: schemas.InRecipeSchema
):
    got = await recipe_service.register_recipe(payload, username="tester")
    want = schemas.RecipeSchema(
        id=got.id,
        name="Burrito",
        ingredients=["beans", "rice", "tortilla"],
        url="http://polloslocos.com/1",
        images=["http://polloslocos.com/images/1"],
        created_by="tester",
    )

    assert got == want


async def test_ingredients_successfully_registered(
    recipe_service: services.RecipeService, payload: schemas.InRecipeSchema
):
    await recipe_service.register_recipe(payload, username="tester")
    ingredients = await recipe_service._ingred_repo.get_all()

    got = sorted(ingredient.name for ingredient in ingredients)
    want = ["beans", "rice", "tortilla"]

    assert got == want


async def test_get_recipes(
    db_session: AsyncSession, recipe_service: services.RecipeService
):
    qry = """
    INSERT OR IGNORE INTO recipes (name, url, images, ingredients, created_by)
    VALUES
        ('Potato Salad', 'http://recipes.com/1', '["http://images.com/1"]', '["potato", "mayo"]', 'testuser'),
        ('Plain Burger', 'http://recipes.com/2', '["http://images.com/2"]', '["beef", "tomato", "mayo"]', 'testuser')
    ;
    """
    await db_session.execute(text(qry))

    got = await recipe_service.get_recipes()
    want = [
        schemas.RecipeSchema(
            id=1,
            name="Potato Salad",
            url="http://recipes.com/1",
            created_by="testuser",
            images=["http://images.com/1"],
            ingredients=["potato", "mayo"],
        ),
        schemas.RecipeSchema(
            id=2,
            name="Plain Burger",
            url="http://recipes.com/2",
            created_by="testuser",
            images=["http://images.com/2"],
            ingredients=["beef", "tomato", "mayo"],
        ),
    ]

    assert got == want


async def test_get_all_none_found(recipe_service: services.RecipeService):
    got = await recipe_service.get_recipes()
    want = []

    assert got == want
