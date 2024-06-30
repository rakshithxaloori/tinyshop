from sqlalchemy import ForeignKey, Text, Boolean, ARRAY, JSON, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class Product(SqlBase):
    __tablename__ = "product"

    id = mapped_column(Text, primary_key=True, default=get_primary_key("prod"))
    name = mapped_column(Text)
    description = mapped_column(Text, nullable=True)
    handle = mapped_column(Text)
    active = mapped_column(Boolean)
    # TODO add images when using postgres
    # images = mapped_column(ARRAY(JSON), nullable=True)
    shippable = mapped_column(Boolean, default=True)
    preorder = mapped_column(Boolean, default=False)

    shop_id = mapped_column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="products")
    options = relationship("Option", back_populates="product")
    variants = relationship("Variant", back_populates="product")

    # discount_config_off_product_id = mapped_column(
    #     Text, ForeignKey("_discount_config_off_product.id")
    # )
    # discount_config_off_product = relationship(
    #     "DiscountOffProductConfig", back_populates="product_discounts"
    # )
    # discount_config_buy_x_get_y_buy_id = mapped_column(
    #     Text, ForeignKey("_discount_config_buy_x_get_y.id"), nullable=True
    # )
    # discount_config_buy_x_get_y_buy = relationship(
    #     "DiscountConfigBuyXGetY", back_populates="products_buy"
    # )
    # discount_config_buy_x_get_y_get_id = mapped_column(
    #     Text, ForeignKey("_discount_config_buy_x_get_y.id"), nullable=True
    # )
    # discount_config_buy_x_get_y_get = relationship(
    #     "DiscountConfigBuyXGetY", back_populates="product_get"
    # )

    __table_args__ = (
        UniqueConstraint("shop_id", "handle", name="unique_product_handle_shop"),
    )
