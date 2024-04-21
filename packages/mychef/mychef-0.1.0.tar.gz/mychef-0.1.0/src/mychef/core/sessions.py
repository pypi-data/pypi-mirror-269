from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from mychef.core.config import settings

engine = create_engine(settings.uri)
async_engine = create_async_engine(settings.async_uri)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
