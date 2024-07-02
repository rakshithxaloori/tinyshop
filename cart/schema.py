from pydantic import BaseModel

from utils.model import PyBaseModel
from utils.object import object_type
from cart.model import CartStatusEnum
from cart.cart_item.schema import CartItemList


class CartItemCreate(BaseModel):
    price: str
    quantity: int


class CartBase(BaseModel):
    pass


class CartCreate(CartBase):
    cart_item: CartItemCreate


class Cart(CartBase, PyBaseModel):
    id: str
    object: str = object_type.CART
    status: CartStatusEnum
    cart_items: CartItemList


class CartList(BaseModel):
    object: str = "list"
    url: str = "/v1/carts"
    has_more: bool
    data: list[Cart] = []


class CartUpdate(BaseModel):
    status: CartStatusEnum


class CartDelete(BaseModel):
    id: str
    object: str = object_type.CART
    deleted: bool
