from pydantic import BaseModel

from app.lib.model import PyBaseModel
from app.lib.object import ObjectType
from app.checkout.model import CheckoutStatusEnum
from app.discount.schema import DiscountList
from app.subscription.schema import SubscriptionList


class CheckoutLineItem(BaseModel):
    price: str
    quantity: int


class CheckoutLineItemList(BaseModel):
    object: str = "list"
    data: list[CheckoutLineItem] = []
    has_more: bool
    url: str = "/v1/checkout_items"  # TODO checkout line item


class CheckoutBase(BaseModel):
    return_url: str
    success_url: str
    url: str
    customer_address: str | None = None


class CheckoutCreate(CheckoutBase):
    customer: str
    cart: str


class Checkout(CheckoutBase, PyBaseModel):
    id: str
    object: str = ObjectType.CHECKOUT
    status: CheckoutStatusEnum
    currency: str
    amount_total: int
    amount_subtotal: int
    amount_discount: int
    amount_shipping: int
    amount_tax: int
    expires_at: int
    customer: str
    # invoice: str | None = None
    # discounts: DiscountList
    subscriptions: SubscriptionList | None = None
    line_items: CheckoutLineItemList


class CheckoutUpdate(BaseModel):
    # ID of UserAddress instance
    customer_address: str


class CheckoutList(BaseModel):
    object: str = "list"
    data: list[Checkout] = []
    has_more: bool
    url: str = "/v1/checkouts"


class CheckoutDelete(BaseModel):
    id: str
    object: str = ObjectType.CHECKOUT
    deleted: bool
