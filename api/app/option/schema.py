from pydantic import BaseModel

from app.lib.model import PyBaseModel
from app.lib.object import ObjectType


class OptionBase(BaseModel):
    name: str
    values: list[str]


class OptionCreate(OptionBase):
    product: str


class Option(OptionBase, PyBaseModel):
    id: str
    object: str = ObjectType.OPTION


class OptionList(BaseModel):
    object: str = "list"
    url: str = "/v1/options"
    has_more: bool
    data: list[Option] = []


class OptionUpdate(BaseModel):
    name: str | None = None
    values: list[str] = []


class OptionDelete(BaseModel):
    id: str
    object: str = ObjectType.OPTION
    deleted: bool
