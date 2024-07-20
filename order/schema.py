from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from order.model import OrderTypeEnum, OrderStatusEnum


class OrderLineItemCreate(BaseModel):
    quantity: int
    price: str


class OrderLineItem(BaseModel):
    quantity: int
    unit_amount: int
    price: str


class OrderBase(BaseModel):
    invoice: str | None = None
    customer: str


class OrderCreate(OrderBase):
    line_items: list[OrderLineItemCreate] = []


class Order(OrderBase, PyBaseModel):
    id: str
    object: str = ObjectType.ORDER
    number: int
    status: OrderStatusEnum
    type: OrderTypeEnum
    line_items: list[OrderLineItem] = []


class OrderList(BaseModel):
    object: str = "list"
    url: str = "/v1/orders"
    data: list[Order] = []
    has_more: bool


class OrderUpdate(BaseModel):
    type: OrderTypeEnum | None = None
    status: OrderStatusEnum | None = None
    # TODO add remove line items?


class OrderDelete(BaseModel):
    id: str
    object: str = ObjectType.ORDER
    deleted: bool
