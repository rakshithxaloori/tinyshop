from sqlalchemy import Column, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class Option(SqlBase):
    __tablename__ = "option"

    id = Column(Text, primary_key=True, default=get_primary_key("opt"))
    name = Column(Text)
    # TODO add values when using postgres
    # values = Column(ARRAY(Text))

    shop_id = Column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="options")
    product_id = Column(Text, ForeignKey("product.id", ondelete="CASCADE"))
    product = relationship("Product", back_populates="options")
