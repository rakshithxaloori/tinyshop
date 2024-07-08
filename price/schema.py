from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from price.enum import PriceTypeEnum, RecurringTypeEnum


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
    default: bool
    customer_unit_amount: CustomerUnitAmount | None = None
    recurring: Recurring | None = None


class PriceCreate(PriceBase):
    variant: str


class Price(PriceBase, PyBaseModel):
    id: str
    object: str = ObjectType.PRICE


class PriceList(BaseModel):
    object: str = "list"
    url: str = "/v1/prices"
    has_more: bool
    data: list[Price] = []


class PriceUpdate(BaseModel):
    active: bool | None = None
    default: bool | None = None
    unit_compare_amount: int | None = None
    customer_unit_amount: CustomerUnitAmount | None = None
    recurring: Recurring | None = None


class PriceDelete(BaseModel):
    id: str
    object: str = ObjectType.PRICE
    deleted: bool
