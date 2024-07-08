from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType

# from price.schema import Price


class CartItemBase(BaseModel):
    quantity: int


class CartItemCreate(CartItemBase):
    cart: str
    price: str


class CartItem(CartItemBase, PyBaseModel):
    id: str
    object: str = ObjectType.CART_ITEM
    price: str  # TODO expand on expand


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
