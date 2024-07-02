from pydantic import BaseModel

from utils.model import PyBaseModel
from utils.object import object_type


class InventoryBase(BaseModel):
    quantity: int


class InventoryCreate(InventoryBase):
    variant: str
    warehouse: str


class Inventory(InventoryBase, PyBaseModel):
    id: str
    object: str = object_type.INVENTORY


class InventoryUpdate(BaseModel):
    quantity: int


class InventoryDelete(BaseModel):
    id: str
    object: str = object_type.INVENTORY
    deleted: bool
