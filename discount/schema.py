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
    code: str
    active: bool
    expires_at: datetime | None = None
    applies_max: int | None = None


class DiscountProductsList(BaseModel):
    object: str = "list"
    url: str = "/v1/discounts/{discount_id}/products"
    has_more: bool
    data: list[Product] | list[str]


class DiscountCustomersList(BaseModel):
    object: str = "list"
    url: str = "/v1/discounts/{discount_id}/customers"
    has_more: bool
    data: list[Customer] | list[str]


class OffProduct(BaseModel):
    quantity_min: int | None = None
    amount_off: int | None = None
    percentage_off: int | None = None
    products: DiscountProductsList | None = None


class OffProductUpdateProducts(BaseModel):
    add: list[str] = []
    remove: list[str] = []


class OffProductUpdate(BaseModel):
    quantity_min: int | None = None
    amount_off: int | None = None
    percentage_off: int | None = None
    products: OffProductUpdateProducts | None = None


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
    products_buy: DiscountProductsList | None = None
    variant_get: str | Variant


class BuyXGetYUpdateProducts(BaseModel):
    add: list[str] = []
    remove: list[str] = []


class BuyXGetYUpdate(BaseModel):
    quantity_min: int | None = None
    amount_min: int | None = None
    quantity_get: int | None = None
    variant_get: str | None = None
    products_buy: BuyXGetYUpdateProducts | None = None


class DiscountConfig(BaseModel):
    off_product: OffProduct | OffProductUpdate | None = None
    off_order: OffOrder | None = None
    shipping: Shipping | None = None
    buy_x_get_y: BuyXGetY | BuyXGetYUpdate | None = None


class DiscountCreate(DiscountBase):
    customers: list[str] | None = None
    config: DiscountConfig


class Discount(DiscountBase, PyBaseModel):
    id: str
    object: str = ObjectType.DISCOUNT
    config: DiscountConfig
    customers: DiscountCustomersList


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
    config: DiscountConfig | None = None


class DiscountDelete(BaseModel):
    id: str
    object: str = ObjectType.DISCOUNT
    deleted: bool
