import pytest
from pydantic_core import Url
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from mychef.core.exceptions import AlreadyExists
from mychef.recipes import repository, schemas


@pytest.fixture
def recipe_repo(db_session: AsyncSession) -> repository.SqlalchemyRecipeRepository:
    return repository.SqlalchemyRecipeRepository(db_session)


@pytest.fixture
def recipe() -> schemas.InRecipeSchema:
    return schemas.InRecipeSchema(
        name="My pumpkin pie",
        url=Url("http://pumpkin.com/recipes/1"),
        ingredients=["pumpkin", "flour", "sugar"],
        images=[Url("http://pumpkin.com/images/1")],
    )


@pytest.fixture
async def with_stored_recipes(db_session: AsyncSession) -> None:
    qry = """
INSERT INTO recipes (name, url, images, ingredients, created_by)
VALUES
    ('Potato Salad', 'http://recipes.com/1', '["http://images.com/1"]', '["potato", "mayo"]', 'tester'),
    ('Plain Burger', 'http://recipes.com/2', '["http://images.com/2"]', '["beef", "tomato", "mayo"]', 'tester'),
    ('Homemade Cereal', 'http://recipes.com/3', '["http://images.com/3"]', '["oats", "milk", "banana"]', 'tester'),
    ('Cheese cake', 'http://recipes.com/4', '["http://images.com/4"]', '["cream cheese", "cookies"]', 'tester'),
    ('Cheesesteak', 'http://recipes.com/5', '["http://images.com/5"]', '["cheese", "beef"]', 'tester')
;
    """
    await db_session.execute(text(qry))


async def test_can_create_recipe(
    recipe_repo: repository.SupportsRecipeRepository, recipe: schemas.InRecipeSchema
):
    got = await recipe_repo.create(recipe, created_by="tester")
    want = schemas.RecipeSchema(
        id=got.id,
        name="My pumpkin pie",
        url="http://pumpkin.com/recipes/1",
        ingredients=["pumpkin", "flour", "sugar"],
        images=["http://pumpkin.com/images/1"],
        created_by="tester",
    )

    assert got == want


async def test_duplicate_recipe_raises(
    recipe_repo: repository.SupportsRecipeRepository, recipe: schemas.InRecipeSchema
):
    await recipe_repo.create(recipe, created_by="tester")
    with pytest.raises(AlreadyExists):
        await recipe_repo.create(recipe, created_by="tester")


@pytest.fixture
def ingredient_repo(
    db_session: AsyncSession,
) -> repository.SqlalchemyIngredientRepository:
    return repository.SqlalchemyIngredientRepository(db_session)


@pytest.fixture
def ingredient() -> schemas.InIngredientSchema:
    return schemas.InIngredientSchema(name="tomato")


async def test_can_create_ingredient(
    ingredient_repo: repository.SupportsIngredientRepository,
    ingredient: schemas.InIngredientSchema,
):
    got = await ingredient_repo.create(ingredient)
    want = schemas.IngredientSchema(id=got.id, name="tomato")

    assert got == want


async def test_duplicate_ingredient_raises(
    ingredient_repo: repository.SupportsIngredientRepository,
    ingredient: schemas.InIngredientSchema,
):
    await ingredient_repo.create(ingredient)
    with pytest.raises(AlreadyExists):
        await ingredient_repo.create(ingredient)


@pytest.mark.usefixtures("with_stored_recipes")
@pytest.mark.parametrize(
    "ingredients, expected_count",
    [
        [["chocolate"], 0],
        [["tomato", "chocolate"], 1],
        [["mayo"], 2],
        [["beef", "potato"], 3],
    ],
)
async def test_find_recipes_with_at_least_one_ingredient_present(
    recipe_repo: repository.SupportsRecipeRepository,
    ingredients: list[str],
    expected_count: int,
):
    results = await recipe_repo.get_by_ingredients(ingredients, must_include_all=False)

    assert len(results) == expected_count


@pytest.mark.usefixtures("with_stored_recipes")
@pytest.mark.parametrize(
    "ingredients, expected_count",
    [
        [["chocolate"], 0],
        [["tomato", "chocolate"], 0],
        [["mayo"], 2],
        [["beef", "potato"], 0],
    ],
)
async def test_find_recipes_with_all_ingredients_present(
    recipe_repo: repository.SupportsRecipeRepository,
    ingredients: list[str],
    expected_count: int,
):
    results = await recipe_repo.get_by_ingredients(ingredients, must_include_all=True)

    assert len(results) == expected_count


@pytest.mark.usefixtures("with_stored_recipes")
@pytest.mark.parametrize(
    "ingredients, expected_count",
    [
        [["cheese"], 1],
        [["cream cheese"], 1],
        [["cheese", "cream cheese"], 2],
    ],
)
async def test_with_absolute_matching(
    recipe_repo: repository.SupportsRecipeRepository,
    ingredients: list[str],
    expected_count: int,
):
    results = await recipe_repo.get_by_ingredients(ingredients, absolute_match=True)

    assert len(results) == expected_count


@pytest.mark.usefixtures("with_stored_recipes")
@pytest.mark.parametrize(
    "ingredients, expected_count",
    [
        [["cheese"], 2],
        [["cream cheese"], 1],
        [["cheese", "cream cheese"], 2],
    ],
)
async def test_without_absolute_matching(
    recipe_repo: repository.SupportsRecipeRepository,
    ingredients: list[str],
    expected_count: int,
):
    results = await recipe_repo.get_by_ingredients(ingredients, absolute_match=False)

    assert len(results) == expected_count
