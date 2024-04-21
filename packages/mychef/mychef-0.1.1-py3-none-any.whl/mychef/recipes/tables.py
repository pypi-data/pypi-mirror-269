from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import JSON, DateTime, Integer, String

from mychef.core.tables import Base


class Ingredient(Base):
    """Ingredient database table mapping."""

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())


class Recipe(Base):
    """Recipe database table mapping."""

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False, unique=True)
    images = Column(JSON, nullable=False)
    ingredients = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(String(255), nullable=False)
