from pydantic import BaseModel

from utils.model import PyBaseModel
from utils.object import object_type


class VariantOptionValue(BaseModel):
    name: str
    value: str


class PackageDimensions(BaseModel):
    height: float
    width: float
    length: float
    weight: float


class VariantBase(BaseModel):
    name: str
    description: str | None = None
    active: bool
    options: list[VariantOptionValue] | None = None
    accept_zero_inventory_orders: bool
    next_refill: int
    package_dimensions: PackageDimensions | None = None


class VariantCreate(VariantBase):
    product: str


class Variant(VariantBase, PyBaseModel):
    id: str
    object: str = object_type.VARIANT


class VariantList(BaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[Variant] = []


class VariantUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    options: list[VariantOptionValue] | None = None
    accept_zero_inventory_orders: bool | None = None
    next_refill: int | None = None
    package_dimensions: PackageDimensions | None = None


class VariantDelete(BaseModel):
    id: str
    object: str = object_type.VARIANT
    deleted: bool
