import enum
from sqlalchemy import Column, Text, ForeignKey, Boolean, String, Enum, Integer
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class PriceTypeEnum(enum.Enum):
    ONE_TIME = "one_time"
    SUBSCRIPTION = "subscription"


class Price(SqlBase):
    __tablename__ = "price"

    id = Column(Text, primary_key=True, default=get_primary_key("price"))
    active = Column(Boolean)
    currency = Column(String(3))
    type = Column(Enum(PriceTypeEnum))
    unit_amount = Column(Integer)

    shop_id = Column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="prices")
    variant_id = Column(Text, ForeignKey("variant.id", ondelete="CASCADE"))
    variant = relationship("Variant", back_populates="prices")

    recurring = relationship("Recurring", back_populates="price")
    customer_unit_amount = relationship("CustomerUnitAmount", back_populates="price")
    cart_items = relationship("CartItems", back_populates="price")


class CustomerUnitAmount(SqlBase):
    __tablename__ = "_customer_unit_amount"

    id = Column(Text, primary_key=True, default=get_primary_key("_cua"))
    maximum = Column(Integer, nullable=True)
    minimum = Column(Integer, nullable=True)
    preset = Column(Integer, default=1)

    price_id = Column(Text, ForeignKey("price.id", ondelete="CASCADE"), unique=True)
    price = relationship("Price", back_populates="customer_unit_amount")


class RecurringTypeEnum(enum.Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class Recurring(SqlBase):
    __tablename__ = "_recurring"

    id = Column(Text, primary_key=True, default=get_primary_key("_recurr"))
    interval = Column(Enum(RecurringTypeEnum))
    interval_count = Column(Integer)

    price_id = Column(Text, ForeignKey("price.id", ondelete="CASCADE"), unique=True)
    price = relationship("Price", back_populates="recurring")
