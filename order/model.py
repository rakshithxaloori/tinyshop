import enum
from sqlalchemy import Column, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class OrderTypeEnum(str, enum.Enum):
    preorder = "preorder"
    deferred = "deferred"
    normal = "normal"


class OrderStatusEnum(str, enum.Enum):
    # TODO
    requires_inventory = "requires_inventory"
    requires_shipping = "requires_shipping"
    shipping = "shipping"
    completed = "completed"
    return_requested = "return_requested"


class Order(SqlBase):
    __tablename__ = "order"

    id = Column(Text, primary_key=True, default=get_primary_key("or"))
    type = Column(Enum(OrderTypeEnum))
    status = Column(Enum(OrderStatusEnum))

    invoice_id = Column(Text, ForeignKey("invoice.id"), nullable=True)
    invoice = relationship("Invoice", back_populates="order")
    customer_id = Column(Text, ForeignKey("customer.id", ondelete="CASCADE"))
    customer = relationship("Customer", back_populates="orders")
    cart_id = Column(Text, ForeignKey("cart.id"))
    cart = relationship("Cart", back_populates="order")
    shippings = relationship("Shipping", back_populates="order")
