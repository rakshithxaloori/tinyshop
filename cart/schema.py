from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from cart.model import CartStatusEnum
from cart_item.schema import CartItemList
from discount.schema import DiscountList


class CartItemCreate(BaseModel):
    price: str
    quantity: int


class CartBase(BaseModel):
    currency: str


class CartCreate(CartBase):
    cart_item: CartItemCreate | None = None


class Cart(CartBase, PyBaseModel):
    id: str
    object: str = ObjectType.CART
    status: CartStatusEnum
    cart_items: CartItemList
    discounts: DiscountList


class CartList(BaseModel):
    object: str = "list"
    url: str = "/v1/carts"
    has_more: bool
    data: list[Cart] = []


class DiscountsUpdate(BaseModel):
    add: list[str] | None = None
    remove: list[str] | None = None


class CartUpdate(BaseModel):
    status: CartStatusEnum | None = None
    discounts: DiscountsUpdate | None = None


class CartDelete(BaseModel):
    id: str
    object: str = ObjectType.CART
    deleted: bool
