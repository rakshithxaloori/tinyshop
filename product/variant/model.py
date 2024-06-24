from sqlalchemy import Column, Text, ForeignKey, Boolean, ARRAY, DateTime, Float
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class Variant(SqlBase):
    __tablename__ = "variant"

    id = Column(Text, primary_key=True, default=get_primary_key("var"))
    name = Column(Text)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=False)
    options = Column(ARRAY(Text))
    accept_zero_inventory_orders = Column(Boolean, default=False)
    next_refill = Column(DateTime, nullable=True)
    unit_label = Column(Text, nullable=True)

    shop_id = Column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="variants")
    product_id = Column(Text, ForeignKey("product.id", ondelete="CASCADE"))
    product = relationship("Product", back_populates="variants")
    default_price_id = Column(Text, ForeignKey("price.id"), nullable=True)
    default_price = relationship("Price", back_populates="variant")
    prices = relationship("Price", back_populates="variant")

    package_dimensions_id = Column(Text, ForeignKey("_package_dimensions.id"))
    package_dimensions = relationship("PackageDimensions", back_populates="variant")


class PackageDimensions(SqlBase):
    __tablename__ = "_package_dimensions"

    id = Column(Text, primary_key=True, default=get_primary_key("_pdim"))
    height = Column(Float)
    width = Column(Float)
    length = Column(Float)
    weight = Column(Float)

    variant_id = Column(Text, ForeignKey("variant.id", ondelete="CASCADE"))
    variant = relationship("Variant", back_populates="package_dimensions")
