from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from price.schema import PriceList


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
    image: str | None = None
    package_dimensions: PackageDimensions | None = None
    is_default: bool


class VariantCreate(VariantBase):
    product: str


class Variant(VariantBase, PyBaseModel):
    id: str
    object: str = ObjectType.VARIANT
    options: str | None
    prices: PriceList | None = None


class VariantList(BaseModel):
    object: str = "list"
    url: str = "/v1/variants"
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
    next_refill: int | None = None
    image: str | None = None
    package_dimensions: PackageDimensionsUpdate | None = None
    is_default: bool | None = None


class VariantDelete(BaseModel):
    id: str
    object: str = ObjectType.VARIANT
    deleted: bool
