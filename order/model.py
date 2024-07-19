from enum import Enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from invoice.model import Invoice
    from customer.model import Customer
    from price.model import Price


class OrderTypeEnum(str, Enum):
    preorder = "preorder"
    deferred = "deferred"
    normal = "normal"


class OrderStatusEnum(str, Enum):
    # TODO
    requires_inventory = "requires_inventory"
    requires_shipping = "requires_shipping"
    shipping = "shipping"
    completed = "completed"
    return_requested = "return_requested"


class Order(SqlBase, table=True):
    id: int = Field(primary_key=True, default_factory=get_primary_key("or"))
    number: int = Field()
    type: OrderTypeEnum = Field()
    status: OrderStatusEnum = Field()

    invoice_id: int = Field(foreign_key="invoice.id", nullable=True)
    invoice: "Invoice" = Relationship(back_populates="order")
    customer_id: int = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="orders")
    # fulfillments = relationship("Fulfillments", back_populates="order")
    # TODO discounts applieds
    line_items: list["OrderLineItem"] = Relationship(back_populates="order")


# TODO order lines
class OrderLineItem(SqlBase, table=True):
    __tablename__ = "_order_line_item"

    id: int = Field(primary_key=True, default_factory=get_primary_key("_oli"))
    quantity: int = Field()
    unit_amount: int = Field()

    order_id: str = Field(foreign_key="order.id")
    order: "Order" = Relationship(back_populates="line_items")
    price_id: str = Field(foreign_key="price.id")
    price: "Price" = Relationship(back_populates="order_line_items")
