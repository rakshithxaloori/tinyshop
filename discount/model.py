import enum
from sqlalchemy import Column, Text, ForeignKey, Boolean, Enum, Integer, DateTime
from sqlalchemy.orm import relationship


from utils.model import SqlBase
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
    type = Column(Enum(DiscountTypeEnum))
    code = Column(Text)
    active = Column(Boolean)
    expires_at = Column(DateTime, nullable=True)

    config_id = Column(Text, ForeignKey("_discount_config.id"))
    config = relationship("DiscountConfig", back_populates="discount")


class DiscountConfig(SqlBase):
    __tablename__ = "_discount_config"

    id = Column(Text, primary_key=True, default=get_primary_key("_dc"))

    discount_id = Column(Text, ForeignKey("discount.id", ondelete="CASCADE"))
    discount = relationship("Discount", back_populates="config")
    off_product_id = Column(
        Text, ForeignKey("_discount_config_off_product.id"), nullable=True
    )
    off_product = relationship("DiscountConfigOffProduct", back_populates="config")
    off_order_id = Column(Text, ForeignKey("_discount_config_off_order.id"))
    off_order = relationship("DiscountConfigOffOrder")
    shipping_id = Column(Text, ForeignKey("_discount_config_shipping.id"))
    shipping = relationship("DiscountConfigShipping")
    buy_x_get_y_id = Column(Text, ForeignKey("_discount_config_buy_x_get_y.id"))
    buy_x_get_y = relationship("DiscountConfigBuyXGetY", back_populates="config")


class DiscountConfigOffProduct(SqlBase):
    __tablename__ = "_discount_config_off_product"

    id = Column(Text, primary_key=True, default=get_primary_key("_dopc"))
    quantity_min = Column(Integer, nullable=True)
    amount_off = Column(Integer, nullable=True)
    percentage_off = Column(Integer, nullable=True)

    product_discounts = relationship(
        "Product", back_populates="discount_config_off_product"
    )
    config_id = Column(Text, ForeignKey("_discount_config.id", ondelete="CASCADE"))
    config = relationship("DiscountConfig", back_populates="off_product")


class DiscountConfigOffOrder(SqlBase):
    __tablename__ = "_discount_config_off_order"

    id = Column(Text, primary_key=True, default=get_primary_key("_dooc"))
    amount_min = Column(Integer, nullable=True)
    amount_off = Column(Integer, nullable=True)
    percentage_off = Column(Integer, nullable=True)

    config_id = Column(Text, ForeignKey("_discount_config.id", ondelete="CASCADE"))


class DiscountConfigShipping(SqlBase):
    __tablename__ = "_discount_config_shipping"

    id = Column(Text, primary_key=True, default=get_primary_key("_dsc"))
    amount_min = Column(Integer, nullable=True)
    amount_off = Column(Integer, nullable=True)
    percentage_off = Column(Integer, nullable=True)


class DiscountConfigBuyXGetY(SqlBase):
    __tablename__ = "_discount_config_buy_x_get_y"

    id = Column(Text, primary_key=True, default=get_primary_key("_dbxgyc"))
    quantity_min = Column(Integer, nullable=True)
    quantity_get = Column(Integer, nullable=True)
    amount_min = Column(Integer, nullable=True)

    products_buy = relationship(
        "Product", back_populates="discount_config_buy_x_get_y_buy"
    )
    product_get_id = Column(Text, ForeignKey("product.id", ondelete="CASCADE"))
    product_get = relationship(
        "Product", back_populates="discount_config_buy_x_get_y_buy"
    )
    variant_get_id = Column(Text, ForeignKey("variant.id", ondelete="CASCADE"))
    variant_get = relationship(
        "Variant", back_populates="discount_config_buy_x_get_y_get"
    )
