from datetime import datetime
from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from discount.model import DiscountTypeEnum
from customer.schema import Customer
from product.schema import Product
from variant.schema import Variant


class DiscountBase(BaseModel):
    type: DiscountTypeEnum
    active: bool
    expires_at: datetime | None = None
    applies_max: int | None = None


class OffProduct(BaseModel):
    quantity_min: int | None = None
    amount_off: int | None = None
    percentage_off: int | None = None
    products: list[str] | list[Product]


class OffOrder(BaseModel):
    quantity_min: int | None = None
    amount_min: int | None = None
    amount_off: int | None = None
    percentage_off: int | None = None


class Shipping(BaseModel):
    quantity_min: int | None = None
    amount_min: int | None = None
    amount_off: int | None = None
    percentage_off: int | None = None


class BuyXGetY(BaseModel):
    quantity_min: int | None = None
    amount_min: int | None = None
    quantity_get: int
    products_buy: list[str] | list[Product]
    variant_get: str | Variant


class DiscountConfig(BaseModel):
    off_product: OffProduct | None = None
    off_order: OffOrder | None = None
    shipping: Shipping | None = None
    buy_x_get_y: BuyXGetY | None = None


class DiscountCreate(DiscountBase):
    customers: list[str] | None = None
    config: DiscountConfig


class DiscountCustomers(BaseModel):
    object: str = "list"
    url: str = "/v1/discounts/{discount_id}/customers"
    has_more: bool
    data: list[Customer]


class Discount(DiscountBase, PyBaseModel):
    id: str
    object: str = ObjectType.DISCOUNT
    config: DiscountConfig
    customers: DiscountCustomers


class DiscountList(BaseModel):
    object: str = "list"
    url: str = "/v1/discounts"
    has_more: bool
    data: list[Discount] = []


class DiscountUpdateCustomers(BaseModel):
    add: list[str] | None = None
    remove: list[str] | None = None


class DiscountUpdate(BaseModel):
    active: bool | None
    expires_at: datetime | None = None
    applies_max: int | None = None

    customers: DiscountUpdateCustomers | None = None


class DiscountDelete(BaseModel):
    id: str
    object: str = ObjectType.DISCOUNT
    deleted: bool
