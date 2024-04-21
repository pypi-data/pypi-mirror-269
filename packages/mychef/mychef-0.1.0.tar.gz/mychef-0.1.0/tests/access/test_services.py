import pydantic
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mychef.access import schemas, services
from mychef.core import exceptions


@pytest.fixture
def access_service(db_session: AsyncSession) -> services.AccessService:
    return services.AccessService.from_session(db_session)


@pytest.fixture
async def user(access_service: services.AccessService) -> schemas.UserSchema:
    user = schemas.UserRegistrationSchema(username="bob", password="password")
    return await access_service._user_repo.create(user)


async def test_authenticate_success(
    access_service: services.AccessService, user: schemas.UserSchema
):
    got = await access_service.authenticate(user.username, "password")
    want = user
    assert got == want


async def test_authenticate_bad_username(access_service: services.AccessService):
    got = await access_service.authenticate("badusername", "password")
    want = None
    assert got == want


async def test_authenticate_bad_pw(
    access_service: services.AccessService, user: schemas.UserSchema
):
    got = await access_service.authenticate(user.username, "badpw")
    want = None
    assert got == want


@pytest.mark.parametrize(
    "creds",
    [
        pytest.param(("testuser", "password" * 100), id="password too long"),
        pytest.param(("testuser" * 100, "password"), id="username too long"),
    ],
)
async def test_register_user_validation(
    access_service: services.AccessService, creds: tuple[str, str]
):
    username, password = creds
    with pytest.raises(pydantic.ValidationError):
        await access_service.register_user(username, password)


async def test_register_user_and_list_usernames(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")

    got = await access_service.list_usernames()
    want = ["testuser"]

    assert got == want


async def test_register_user_already_exists(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")

    got = await access_service.check_username_exists("testuser")
    want = True

    assert got == want


async def test_check_username_does_not_exists(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")

    got = await access_service.check_username_exists("baduser")
    want = False

    assert got == want


async def test_duplicate_user_registration(access_service: services.AccessService):
    await access_service.register_user("testuser", "password")
    with pytest.raises(exceptions.AlreadyExists):
        await access_service.register_user("testuser", "password")
