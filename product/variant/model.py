from sqlalchemy import Column, Text, ForeignKey, Boolean, ARRAY, DateTime, Float
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class Variant(SqlBase):
    __tablename__ = "variant"

    id = Column(Text, primary_key=True, default=get_primary_key("var"))
    name = Column(Text)
    description = Column(Text, nullable=True)
    active = Column(Boolean)
    # TODO add options when using postgres
    # options = Column(ARRAY(Text))
    accept_zero_inventory_orders = Column(Boolean, default=False)
    next_refill = Column(DateTime, nullable=True)
    unit_label = Column(Text, nullable=True)

    shop_id = Column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="variants")
    product_id = Column(Text, ForeignKey("product.id", ondelete="CASCADE"))
    product = relationship("Product", back_populates="variants")
    default_price = relationship("Price", back_populates="variant")
    prices = relationship("Price", back_populates="variant")

    package_dimensions = relationship("PackageDimensions", back_populates="variant")
    inventories = relationship("Inventory", back_populates="variant")
    subscriptions = relationship("Subscription", back_populates="variant")
    shipping_lines = relationship("ShippingLines", back_populates="variant")
    # discount_config_buy_x_get_y_get_id = Column(
    #     Text, ForeignKey("_discount_config_buy_x_get_y.id"), nullable=True
    # )
    # discount_config_buy_x_get_y_get = relationship(
    #     "DiscountConfigBuyXGetY", back_populates="variant_get"
    # )


class PackageDimensions(SqlBase):
    __tablename__ = "_package_dimensions"

    id = Column(Text, primary_key=True, default=get_primary_key("_pdim"))
    height = Column(Float)
    width = Column(Float)
    length = Column(Float)
    weight = Column(Float)

    variant_id = Column(Text, ForeignKey("variant.id", ondelete="CASCADE"), unique=True)
    variant = relationship("Variant", back_populates="package_dimensions")
