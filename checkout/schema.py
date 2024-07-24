from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from checkout.model import CheckoutStatusEnum
from discount.schema import DiscountList


class CheckoutBase(BaseModel):
    return_url: str
    success_url: str
    url: str


class CheckoutCreate(CheckoutBase):
    customer: str
    customer_address: str | None = None
    cart: str


class Checkout(CheckoutBase, PyBaseModel):
    id: str
    object: str = ObjectType.CHECKOUT
    status: CheckoutStatusEnum
    amount_total: int
    amount_subtotal: int
    amount_discount: int
    amount_shipping: int
    amount_tax: int
    expires_at: int
    customer: str
    customer_address: str
    invoice: str | None = None
    discounts: DiscountList


class CheckoutUpdate(BaseModel):
    # ID of CustomerAddress instance
    customer_address: str | None = None


class CheckoutList(BaseModel):
    object: str = "list"
    data: list[Checkout] = []
    has_more: bool
    url: str = "/v1/checkouts"


class CheckoutDelete(BaseModel):
    id: str
    object: str = ObjectType.CHECKOUT
    deleted: bool
