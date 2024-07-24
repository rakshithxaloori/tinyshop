import time
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


def now_timestamp_factory():
    return int(time.time())


class PyBaseModel(BaseModel):
    created: int
    updated: int
    livemode: bool
    # TODO
    # metadata: dict


class SqlBase(SQLModel, table=False):
    created: int = Field(default_factory=now_timestamp_factory)
    updated: int = Field(
        default_factory=now_timestamp_factory,
        sa_column_kwargs={"onupdate": now_timestamp_factory},
    )
    livemode: bool = Field()
    # TODO
    # metadata_ = Field(default={})
