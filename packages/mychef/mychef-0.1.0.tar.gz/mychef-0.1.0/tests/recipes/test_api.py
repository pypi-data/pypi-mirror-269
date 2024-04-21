from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from mychef.access.services import AccessService

Headers = dict[str, str]
"""Helper alias for request header (only for testing)."""

Payload = dict[str, Any]
"""Helper alias for request payload (only for testing)."""


@pytest.fixture
async def with_stored_recipes(db_session: AsyncSession) -> None:
    qry = """
INSERT INTO recipes (name, url, images, ingredients, created_by)
VALUES
    ('Potato Salad', 'http://recipes.com/1', '["http://images.com/1"]', '["potato", "mayo"]', 'tester'),
    ('Plain Burger', 'http://recipes.com/2', '["http://images.com/2"]', '["beef", "tomato", "mayo"]', 'tester')
;
    """
    await db_session.execute(text(qry))


@pytest.fixture
def headers() -> Headers:
    token = AccessService.create_access_token(username="testuser")
    return {"authorization": f"Bearer {token}"}


def test_create_recipe(client: TestClient, headers: Headers):
    payload = {
        "name": "Falafel",
        "url": "http://recipes.com/3",
        "images": ["http://images.com/3"],
        "ingredients": ["chickpeas", "onions"],
    }
    response = client.post("/api/recipes", headers=headers, json=payload)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.usefixtures("with_stored_recipes")
def test_create_recipe_already_exists(client: TestClient, headers: Headers):
    payload = {
        "name": "Potato Salad",
        "url": "http://recipes.com/1",
        "images": ["http://images.com/1"],
        "ingredients": ["potato", "mayo"],
    }
    response = client.post("/api/recipes", headers=headers, json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_recipe_unauthorized(client: TestClient):
    payload = {
        "name": "Falafel",
        "url": "http://recipes.com/3",
        "images": ["http://images.com/3"],
        "ingredients": ["chickpeas", "onions"],
    }
    response = client.post("/api/recipes", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {},
            id="empty payload",
        ),
        pytest.param(
            {
                "name": "Falafel",
                "url": "recipesdotcom",
                "images": ["http://images.com/3"],
                "ingredients": ["chickpeas", "onions"],
            },
            id="bad url",
        ),
        pytest.param(
            {
                "name": "Falafel",
                "url": "http://recipes.com/3",
                "images": ["images/3"],
                "ingredients": ["chickpeas", "onions"],
            },
            id="bad image url",
        ),
    ],
)
def test_create_recipe_with_bad_payload(
    client: TestClient, headers: Headers, payload: Payload
):
    response = client.post("/api/recipes", headers=headers, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.usefixtures("with_stored_recipes")
def test_get_recipes(client: TestClient):
    response = client.get("/api/recipes")
    assert response.status_code == status.HTTP_200_OK
