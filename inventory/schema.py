from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType


class InventoryBase(BaseModel):
    quantity: int


class InventoryCreate(InventoryBase):
    variant: str
    warehouse: str


class Inventory(InventoryBase, PyBaseModel):
    id: str
    object: str = ObjectType.INVENTORY
    warehouse: str
    variant: str


class InventoryUpdate(BaseModel):
    quantity: int


class InventoryDelete(BaseModel):
    id: str
    object: str = ObjectType.INVENTORY
    deleted: bool
