import enum
from sqlalchemy import Column, Text, ForeignKey, Boolean, Enum, Integer, DateTime
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class DiscountTypeEnum(enum.Enum):
    OFF_PRODUCT = "off_product"
    OFF_ORDER = "off_order"
    SHIPPING = "shipping"
    BUY_X_GET_Y = "buy_x_get_y"


class Discount(SqlBase):
    # TODO
    __tablename__ = "discount"

    id = Column(Text, primary_key=True, default=get_primary_key("dis"))
    code = Column(Text)
    active = Column(Boolean)
    type = Column(Enum(DiscountTypeEnum))
    amount_off = Column(Integer, nullable=True)
    percentage_off = Column(Integer, nullable=True)
    expires_at = Column(DateTime, nullable=True)
