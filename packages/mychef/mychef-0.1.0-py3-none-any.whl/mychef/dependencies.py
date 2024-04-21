from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import mychef.access.repository
import mychef.access.services
import mychef.recipes.repository
import mychef.recipes.services
from mychef.core import exceptions, http_exceptions, oauth, sessions

AuthBearer = Annotated[oauth.Token, Depends(oauth.oauth2_scheme)]
AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Async session to inject into API endpoints."""
    async with sessions.async_session() as session:
        yield session
        await session.commit()


DBSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_access_service(db: DBSession) -> mychef.access.services.AccessService:
    """Instantiate access service."""
    return mychef.access.services.AccessService.from_session(db)


AccessService = Annotated[
    mychef.access.services.AccessService, Depends(get_access_service)
]


def get_recipe_service(db: DBSession) -> mychef.recipes.services.RecipeService:
    """Instantiate recipe service."""
    return mychef.recipes.services.RecipeService.from_session(db)


RecipeService = Annotated[
    mychef.recipes.services.RecipeService, Depends(get_recipe_service)
]


def get_username_from_bearer_token(token: AuthBearer) -> str:
    try:
        payload = oauth.decode_token(token)
    except exceptions.Unauthorized as err:
        raise http_exceptions.InvalidCredentials from err
    else:
        return str(payload.get("sub", ""))


UsernameFromBearerToken = Annotated[str, Depends(get_username_from_bearer_token)]
