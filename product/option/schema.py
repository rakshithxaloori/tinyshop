from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import object_type


class OptionBase(BaseModel):
    name: str
    values: list[str]


class OptionCreate(OptionBase):
    pass


class Option(OptionBase, PyBaseModel):
    id: str
    object: str = object_type.OPTION


class OptionList(BaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[Option] = []


class OptionUpdate(BaseModel):
    name: str | None = None
    values: list[str] = []


class OptionDelete(BaseModel):
    id: str
    object: str = object_type.OPTION
    deleted: bool
