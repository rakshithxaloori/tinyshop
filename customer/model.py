from sqlalchemy import Column, Text, ForeignKey, String
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class Customer(SqlBase):
    __tablename__ = "customer"

    id = Column(Text, primary_key=True, default=get_primary_key("cus"))
    name = Column(Text)
    email = Column(Text, nullable=True)
    phone = Column(Text)

    shop_id = Column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="customers")
    addresses = relationship("CustomerAddress", back_populates="customer")
    checkouts = relationship("Checkout", back_populates="customer")
    subscriptions = relationship("Subscription", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")
    orders = relationship("Order", back_populates="customer")


class CustomerAddress(SqlBase):
    __tablename__ = "customer_address"

    id = Column(Text, primary_key=True, default=get_primary_key("caddr"))
    name = Column(Text)
    line1 = Column(Text)
    line2 = Column(Text, nullable=True)
    city = Column(Text)
    state = Column(Text)
    country = Column(String(2))
    postal_code = Column(Text)

    customer_id = Column(Text, ForeignKey("customer.id", ondelete="CASCADE"))
    customer = relationship("Customer", back_populates="addresses")
