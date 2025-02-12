from pydantic import BaseModel

from app.lib.model import PyBaseModel
from app.lib.object import ObjectType
from app.discount.model import DiscountTypeEnum


class DiscountBase(BaseModel):
    type: DiscountTypeEnum
    code: str
    active: bool
    expires_at: int | None = None
    applies_max: int | None = None


class DiscountProductsList(BaseModel):
    object: str = "list"
    url: str = "/v1/discounts/{discount_id}/products"
    has_more: bool
    data: list[str]


class DiscountCustomersList(BaseModel):
    object: str = "list"
    url: str = "/v1/discounts/{discount_id}/customers"
    has_more: bool
    data: list[str]


class OffProduct(BaseModel):
    quantity_min: int | None = None
    amount_off: int | None = None
    percentage_off: int | None = None
    products: DiscountProductsList | list[str] | None = None


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
    products_buy: DiscountProductsList | list[str] | None = None
    variant_get: str


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
    data: list[Discount] | list[str] = []


class DiscountUpdateCustomers(BaseModel):
    add: list[str] | None = None
    remove: list[str] | None = None


class DiscountUpdate(BaseModel):
    active: bool | None = None
    expires_at: int | None = None
    applies_max: int | None = None

    customers: DiscountUpdateCustomers | None = None
    config: DiscountConfig | None = None


class DiscountDelete(BaseModel):
    id: str
    object: str = ObjectType.DISCOUNT
    deleted: bool
