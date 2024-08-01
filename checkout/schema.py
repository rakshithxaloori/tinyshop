from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from checkout.model import CheckoutStatusEnum
from discount.schema import DiscountList
from subscription.schema import SubscriptionList


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
    customer_address: str | None = None
    status: CheckoutStatusEnum | None = None


class CheckoutList(BaseModel):
    object: str = "list"
    data: list[Checkout] = []
    has_more: bool
    url: str = "/v1/checkouts"


class CheckoutDelete(BaseModel):
    id: str
    object: str = ObjectType.CHECKOUT
    deleted: bool
