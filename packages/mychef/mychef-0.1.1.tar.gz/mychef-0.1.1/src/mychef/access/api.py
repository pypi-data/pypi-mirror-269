from urllib.parse import unquote

from fastapi import APIRouter

from mychef import dependencies
from mychef.core import http_exceptions

from . import schemas

router = APIRouter(prefix="/auth", tags=["access"])


@router.post("/token", summary="Generates access token when passed valid credentials.")
async def handle_generate_access_token(
    form: dependencies.AuthForm,
    access_service: dependencies.AccessService,
) -> schemas.AccessToken:
    """Defines endpoint for generating access tokens."""
    user = await access_service.authenticate(form.username, unquote(form.password))

    if not user:
        raise http_exceptions.InvalidCredentials

    token = access_service.create_access_token(user.username)

    return schemas.AccessToken(access_token=token, token_type="bearer")


@router.get("/me", summary="Fetches information regarding current user.")
async def handle_get_current_user(
    username: dependencies.UsernameFromBearerToken,
    access_service: dependencies.AccessService,
) -> schemas.UserPublicSchema:
    """Defines endpoint for fetching information for the current user."""
    if await access_service.check_username_exists(username):
        return schemas.UserPublicSchema(username=username)

    raise http_exceptions.InvalidCredentials
