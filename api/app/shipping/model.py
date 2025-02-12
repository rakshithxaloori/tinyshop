import enum
from sqlalchemy import Column, Text, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


class ShippingStatusEnum(str, enum.Enum):
    queued = "queued"
    dispatched = "dispatched"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    delivery_attemmpted = "delivery_attempted"
    returned = "returned"
    canceled = "canceled"


class Shipping(SqlBase):
    id = Column(Text, primary_key=True, default_factory=get_primary_key("sh"))
    status = Column(Enum(ShippingStatusEnum))

    order_id = Column(Text, ForeignKey("order.id", ondelete="CASCADE"))
    order = relationship("Order", back_populates="shippings")
    shipping_lines = relationship("ShippingLines", back_populates="shipping")
    warehouse_id = Column(Text, ForeignKey("warehouse.id"))
    warehouse = relationship("Warehouse", back_populates="shippings")
    shipping_address_id = Column(Text, ForeignKey("shipping_address.id"))
    shipping_address = relationship("ShippingAddress", back_populates="shipping")


class ShippingLineItem(SqlBase):
    __tablename__ = "_shipping_line_item"

    id = Column(Text, primary_key=True, default_factory=get_primary_key("sl"))
    quantity = Column(Integer)

    shipping_id = Column(Text, ForeignKey("shipping.id", ondelete="CASCADE"))
    variant_id = Column(Text, ForeignKey("variant.id"))
    variant = relationship("Variant", back_populates="shipping_lines")


class ShippingAddress(SqlBase):
    __tablename__ = "_shipping_address"

    id = Column(Text, primary_key=True, default_factory=get_primary_key("_saddr"))
    name = Column(Text)
    email = Column(Text, nullable=True)
    phone = Column(Text)
    line1 = Column(Text)
    line2 = Column(Text, nullable=True)
    city = Column(Text)
    state = Column(Text)
    country = Column(String(2))
    postal_code = Column(Text)

    shipping_id = Column(Text, ForeignKey("shipping.id", ondelete="CASCADE"))
