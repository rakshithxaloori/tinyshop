from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class PyBaseModel(BaseModel):
    created: int
    updated: int
    livemode: bool
    # TODO
    # metadata: dict


class SqlBase(SQLModel, table=False):
    created: datetime = Field(default=datetime.now())
    updated: datetime = Field(default=datetime.now())
    livemode: bool = Field()
    # TODO
    # metadata_ = Field(default={})
