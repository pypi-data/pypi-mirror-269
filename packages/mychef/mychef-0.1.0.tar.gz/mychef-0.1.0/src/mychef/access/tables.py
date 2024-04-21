from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from mychef.core.tables import Base


class User(Base):
    """User database table mapping."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=func.now())
