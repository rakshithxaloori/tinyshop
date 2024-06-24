from sqlalchemy import Column, ForeignKey, Text, Boolean, ARRAY, URL
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class Product(SqlBase):
    __tablename__ = "product"

    id = Column(Text, primary_key=True, default=get_primary_key("prod"))
    name = Column(Text)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=False)
    images = Column(ARRAY(URL))
    shippable = Column(Boolean, default=True)
    preorder = Column(Boolean, default=False)

    shop_id = Column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="products")
    options = relationship("Option", back_populates="product")
    variants = relationship("Variant", back_populates="product")
