from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import object_type
from product.price.schema import Price


class CartItemBase(BaseModel):
    quantity: int


class CartItemCreate(CartItemBase):
    cart: str
    price: str


class CartItem(CartItemBase, PyBaseModel):
    id: str
    object: str = object_type.CART_ITEM
    price: Price


class CartItemList(BaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[CartItem] = []


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemDelete(BaseModel):
    id: str
    object: str = object_type.CART_ITEM
    deleted: bool
