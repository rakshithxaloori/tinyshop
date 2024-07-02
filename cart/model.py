import enum
from sqlalchemy import Column, Text, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class CartStatusEnum(str, enum.Enum):
    REQUIRES_PAYMENT = "requires_payment"
    ABANDONED = "abandoned"
    PAID = "paid"


class Cart(SqlBase):
    __tablename__ = "cart"

    id = Column(Text, primary_key=True, default=get_primary_key("cart"))
    status = Column(Enum(CartStatusEnum), default=CartStatusEnum.REQUIRES_PAYMENT)

    items = relationship("CartItem", back_populates="cart")
    discounts = relationship("Discount", back_populates="carts")
    checkouts = relationship("Checkout", back_populates="cart")
    invoices = relationship("Invoice", back_populates="cart")
    order_id = Column(Text, ForeignKey("order.id"))
    order = relationship("Order", back_populates="cart")


class CartItem(SqlBase):
    __tablename__ = "cart_item"

    id = Column(Text, primary_key=True, default=get_primary_key("ci"))
    quantity = Column(Integer)

    cart_id = Column(Text, ForeignKey("cart.id", ondelete="CASCADE"))
    cart = relationship("Cart", back_populates="items")
    price_id = Column(Text, ForeignKey("price.id", ondelete="CASCADE"))
    price = relationship("Price", back_populates="cart_items")
