from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, JSON
from sqlalchemy.sql import func

from database import Base


class PyBaseModel(BaseModel):
    created: int
    updated: int
    livemode: bool
    metadata: dict


class SqlBase(Base):
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
    livemode = Column(Boolean)
    metadata = Column(JSON, default={})
