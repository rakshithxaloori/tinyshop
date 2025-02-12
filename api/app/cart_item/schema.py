from pydantic import BaseModel

from app.lib.model import PyBaseModel
from app.lib.object import ObjectType


class CartItemBase(BaseModel):
    quantity: int


class CartItemCreate(CartItemBase):
    cart: str
    price: str


class CartItem(CartItemBase, PyBaseModel):
    id: str
    object: str = ObjectType.CART_ITEM
    price: str


class CartItemList(BaseModel):
    object: str = "list"
    url: str  # TODO
    has_more: bool
    data: list[CartItem] = []


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemDelete(BaseModel):
    id: str
    object: str = ObjectType.CART_ITEM
    deleted: bool
