from sqlalchemy import Column, ForeignKey, Text, String
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class Address(SqlBase):
    __tablename__ = "addresses"

    id = Column(Text, primary_key=True, default=get_primary_key("addr"))
    name = Column(Text)
    line1 = Column(Text)
    line2 = Column(Text, nullable=True)
    city = Column(Text)
    state = Column(Text)
    country = Column(String(2))
    postal_code = Column(Text)

    customer_id = Column(Text, ForeignKey("customers.id", ondelete="CASCADE"))
    customer = relationship("Customer", back_populates="addresses")
