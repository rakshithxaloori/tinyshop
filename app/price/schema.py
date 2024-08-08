from pydantic import BaseModel

from app.lib.model import PyBaseModel
from app.lib.object import ObjectType
from app.price.enum import PriceTypeEnum, RecurringTypeEnum


class CustomerUnitAmount(BaseModel):
    maximum: int | None = None
    minimum: int | None = None
    preset: int = 1


class Recurring(BaseModel):
    interval: RecurringTypeEnum
    interval_count: int


class PriceBase(BaseModel):
    active: bool
    currency: str
    type: PriceTypeEnum
    unit_amount: int
    unit_compare_amount: int | None = None
    is_default: bool
    customer_unit_amount: CustomerUnitAmount | None = None
    recurring: Recurring | None = None
    variant: str


class PriceCreate(PriceBase):
    pass


class Price(PriceBase, PyBaseModel):
    id: str
    object: str = ObjectType.PRICE
    product: str


class PriceList(BaseModel):
    object: str = "list"
    url: str = "/v1/prices"
    has_more: bool
    data: list[Price] = []


class PriceUpdate(BaseModel):
    active: bool | None = None
    is_default: bool | None = None
    unit_compare_amount: int | None = None
    customer_unit_amount: CustomerUnitAmount | None = None
    recurring: Recurring | None = None


class PriceDelete(BaseModel):
    id: str
    object: str = ObjectType.PRICE
    deleted: bool
