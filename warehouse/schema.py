from pydantic import BaseModel

from utils.model import PyBaseModel
from utils.object import object_type


class WarehouseAddress(BaseModel):
    line1: str
    line2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str


class WarehouseBase(BaseModel):
    name: str
    active: bool
    phone: str
    address: WarehouseAddress


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase, PyBaseModel):
    id: str
    object: str = object_type.WAREHOUSE


class WarehouseList(BaseModel):
    object: str = "list"
    url: str = "/v1/warehouses"
    has_more: bool
    data: list[Warehouse] = []


class WarehouseUpdate(BaseModel):
    name: str | None = None
    active: bool | None = None
    phone: str | None = None
    address: WarehouseAddress | None


class WarehouseDelete(BaseModel):
    id: str
    object: str = object_type.WAREHOUSE
    deleted: bool
