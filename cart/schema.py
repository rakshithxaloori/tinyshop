from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from cart.model import CartStatusEnum
from cart_item.schema import CartItemList


class CartItemCreate(BaseModel):
    price: str
    quantity: int


class CartBase(BaseModel):
    pass


class CartCreate(CartBase):
    cart_item: CartItemCreate | None = None


class Cart(CartBase, PyBaseModel):
    id: str
    object: str = ObjectType.CART
    status: CartStatusEnum
    cart_items: CartItemList


class CartList(BaseModel):
    object: str = "list"
    url: str = "/v1/carts"
    has_more: bool
    data: list[Cart] = []


class CartUpdate(BaseModel):
    status: CartStatusEnum | None = None


class CartDelete(BaseModel):
    id: str
    object: str = ObjectType.CART
    deleted: bool
