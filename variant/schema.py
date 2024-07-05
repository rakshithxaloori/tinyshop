from pydantic import BaseModel
from datetime import datetime

from lib.model import PyBaseModel
from lib.object import object_type


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
    next_refill: datetime
    package_dimensions: PackageDimensions | None = None


class VariantCreate(VariantBase):
    product: str


class Variant(VariantBase, PyBaseModel):
    id: str
    object: str = object_type.VARIANT
    options: str | None


class VariantList(BaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[Variant] = []


class PackageDimensionsUpdate(BaseModel):
    height: float | None = None
    width: float | None = None
    length: float | None = None
    weight: float | None = None


class VariantUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    options: list[VariantOptionValue] | None = None
    accept_zero_inventory_orders: bool | None = None
    next_refill: datetime | None = None
    package_dimensions: PackageDimensionsUpdate | None = None


class VariantDelete(BaseModel):
    id: str
    object: str = object_type.VARIANT
    deleted: bool
