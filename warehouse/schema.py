from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType


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
    object: str = ObjectType.WAREHOUSE


class WarehouseList(BaseModel):
    object: str = "list"
    url: str = "/v1/warehouses"
    has_more: bool
    data: list[Warehouse] = []


class WarehouseAddressUpdate(BaseModel):
    line1: str | None = None
    line2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class WarehouseUpdate(BaseModel):
    name: str | None = None
    active: bool | None = None
    phone: str | None = None
    address: WarehouseAddressUpdate | None


class WarehouseDelete(BaseModel):
    id: str
    object: str = ObjectType.WAREHOUSE
    deleted: bool
