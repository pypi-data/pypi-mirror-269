import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from mychef.access import repository, schemas
from mychef.core.exceptions import AlreadyExists, DoesNotExist


@pytest.fixture
async def repo(db_session: AsyncSession) -> repository.SqlalchemyUserRepository:
    qry = "INSERT INTO users (username, password) VALUES ('admin', 'password');"
    await db_session.execute(text(qry))

    return repository.SqlalchemyUserRepository(db_session)


@pytest.fixture
def user() -> schemas.UserRegistrationSchema:
    return schemas.UserRegistrationSchema(username="bob", password="password")


async def test_create_user_hashes_password(
    repo: repository.SupportsUserRepository, user: schemas.UserRegistrationSchema
):
    db_user = await repo.create(user)
    assert db_user.username == "bob"
    assert db_user.password.startswith("$argon2")


async def test_can_create_user(
    repo: repository.SupportsUserRepository, user: schemas.UserRegistrationSchema
):
    got = await repo.create(user)
    want = schemas.UserSchema(
        id=got.id,
        username="bob",
        password=got.password,  # dynamically hashed password
    )

    assert got == want


async def test_duplicate_user_raises(
    repo: repository.SupportsUserRepository, user: schemas.UserRegistrationSchema
):
    await repo.create(user)
    with pytest.raises(AlreadyExists):
        await repo.create(user)


async def test_user_is_found_by_username(repo: repository.SupportsUserRepository):
    got = await repo.get_by_username("admin")
    want = schemas.UserSchema(
        id=got.id,
        username="admin",
        password="password",
    )

    assert got == want


async def test_user_is_not_found_by_username(repo: repository.SupportsUserRepository):
    with pytest.raises(DoesNotExist):
        await repo.get_by_username("nobody")
