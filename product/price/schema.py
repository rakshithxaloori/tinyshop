import enum
from pydantic import BaseModel

from utils.model import PyBaseModel
from utils.object import object_type
from product.price.model import PriceTypeEnum, RecurringTypeEnum


class CustomerUnitAmount(BaseModel):
    maximum: int | None = None
    minimum: int | None = None
    preset: int


class Recurring(BaseModel):
    interval: RecurringTypeEnum
    interval_count: int


class PriceBase(BaseModel):
    active: bool
    currency: str
    type: PriceTypeEnum
    unit_amount: int
    default: bool
    customer_unit_amount: CustomerUnitAmount | None
    recurring: Recurring | None


class PriceCreate(PriceBase):
    variant: str


class Price(PriceBase, PyBaseModel):
    id: str
    object: object_type.PRICE


class PriceList(BaseModel):
    object: str = "list"
    url: str = "/v1/prices"
    has_more: bool
    data: list[Price] = []


class PriceUpdate(BaseModel):
    active: bool | None = None
    default: bool | None = None
    customer_unit_amount: CustomerUnitAmount | None = None
    recurring: Recurring | None = None


class PriceDelete(BaseModel):
    id: str
    object: str = object_type.PRICE
    deleted: bool
