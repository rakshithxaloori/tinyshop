import time
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class PyBaseModel(BaseModel):
    created: int
    updated: int
    livemode: bool
    # TODO
    # metadata: dict


class SqlBase(SQLModel, table=False):
    created: int = Field(default_factory=lambda _: int(time.time()))
    updated: int = Field(
        default_factory=lambda _: int(time.time()),
        sa_column_kwargs={"onupdate": lambda _: int(time.time())},
    )
    livemode: bool = Field()
    # TODO
    # metadata_ = Field(default={})
