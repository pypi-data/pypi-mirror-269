from __future__ import annotations

import dataclasses
import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from mychef.core import exceptions, hashing, oauth

from . import repository, schemas


@dataclasses.dataclass(frozen=True)
class AccessService:
    """The service layer for the access domain."""

    _user_repo: repository.SupportsUserRepository

    @classmethod
    def from_session(cls, session: AsyncSession) -> AccessService:
        """Build access service from database session."""
        return cls(_user_repo=repository.SqlalchemyUserRepository(session))

    async def authenticate(
        self, username: str, password: str
    ) -> Optional[schemas.UserSchema]:
        """Check that input credentials match the user's stored credentials."""
        try:
            user = await self._user_repo.get_by_username(username)
        except exceptions.DoesNotExist:
            return None

        if not hashing.pwd_context.verify(password, user.password):
            return None

        return user

    async def check_username_exists(self, username: str) -> bool:
        """Check if username exists."""
        try:
            await self._user_repo.get_by_username(username)
        except exceptions.DoesNotExist:
            return False
        else:
            return True

    async def register_user(self, username: str, password: str) -> schemas.UserSchema:
        """Register user given valid username and password."""
        user = schemas.UserRegistrationSchema(username=username, password=password)
        return await self._user_repo.create(user)

    async def list_usernames(self) -> list[str]:
        """List out all persisted usernames."""
        return [user.username for user in await self._user_repo.get_all()]

    @staticmethod
    def create_access_token(username: str, minutes: int = 60) -> oauth.Token:
        """Generate user access token for a duration of time."""
        payload: oauth.TokenPayload = {
            "sub": username,
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(minutes=minutes),
        }
        return oauth.encode_token(payload)
