from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class Customer(SqlBase):
    __tablename__ = "customers"

    id = Column(Text, primary_key=True, default=get_primary_key("cus"))
    name = Column(Text)
    email = Column(Text, nullable=True)
    phone = Column(Text)

    shop_id = Column(Text, ForeignKey("shops.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="customers")
    addresses = relationship("Address", back_populates="customer")
