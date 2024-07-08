import enum
from typing import TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key

# from lib.many_to_many_tables import DiscountCustomerLink

if TYPE_CHECKING:
    from shop.model import Shop
    from product.model import Product
    from variant.model import Variant
    from customer.model import Customer


class DiscountTypeEnum(str, enum.Enum):
    OFF_PRODUCT = "off_product"
    OFF_ORDER = "off_order"
    SHIPPING = "shipping"
    BUY_X_GET_Y = "buy_x_get_y"


class Discount(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("dis"))
    type: DiscountTypeEnum = Field()
    code: str = Field()
    active: bool = Field()
    expires_at: datetime = Field(nullable=True)
    applies_max: int = Field(nullable=True)

    # This Discount is only available for these customers
    # TODO discount
    # customers_select: list["Customer"] = Relationship(
    #     back_populates="discounts_available",
    #     link_model=DiscountCustomerLink,
    # )

    config: "DiscountConfig" = Relationship(
        back_populates="discount",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="discounts")


class DiscountConfig(SqlBase, table=True):
    __tablename__ = "_discount_config"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_dc"))

    discount_id: str = Field(foreign_key="discount.id", unique=True)
    discount: "Discount" = Relationship(back_populates="config")
    off_product: "DiscountConfigOffProduct" = Relationship(
        back_populates="config",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    off_order: "DiscountConfigOffOrder" = Relationship(
        back_populates="config",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    shipping: "DiscountConfigShipping" = Relationship(
        back_populates="config",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    buy_x_get_y: "DiscountConfigBuyXGetY" = Relationship(
        back_populates="config",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class DiscountConfigOffProduct(SqlBase, table=True):
    __tablename__ = "_discount_config_off_product"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_dopc"))
    quantity_min: int = Field(nullable=True)
    amount_off: int = Field(nullable=True)
    percentage_off: int = Field(nullable=True)

    products: list["Product"] = Relationship(
        back_populates="discount_config_off_product"
    )
    config_id: str = Field(
        foreign_key="_discount_config.id",
        unique=True,
    )
    config: "DiscountConfig" = Relationship(back_populates="off_product")


class DiscountConfigOffOrder(SqlBase, table=True):
    __tablename__ = "_discount_config_off_order"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_dooc"))
    quantity_min: int = Field(nullable=True)
    amount_min: int = Field(nullable=True)
    amount_off: int = Field(nullable=True)
    percentage_off: int = Field(nullable=True)

    config_id: str = Field(
        foreign_key="_discount_config.id",
        unique=True,
    )
    config: "DiscountConfig" = Relationship(back_populates="off_order")


class DiscountConfigShipping(SqlBase, table=True):
    __tablename__ = "_discount_config_shipping"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_dsc"))
    quantity_min: int = Field(nullable=True)
    amount_min: int = Field(nullable=True)
    amount_off: int = Field(nullable=True)
    percentage_off: int = Field(nullable=True)

    config_id: str = Field(
        foreign_key="_discount_config.id",
        unique=True,
    )
    config: "DiscountConfig" = Relationship(back_populates="shipping")


class DiscountConfigBuyXGetY(SqlBase, table=True):
    __tablename__ = "_discount_config_buy_x_get_y"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_dbxgyc"))
    quantity_min: int = Field(nullable=True)
    amount_min: int = Field(nullable=True)
    quantity_get: int = Field()

    products_buy: list["Product"] = Relationship(
        back_populates="discount_config_buy_x_get_y"
    )
    variant_get_id: str = Field(foreign_key="variant.id")
    variant_get: "Variant" = Relationship(back_populates="discount_config_buy_x_get_y")
    config_id: str = Field(
        foreign_key="_discount_config.id",
        unique=True,
    )
    config: "DiscountConfig" = Relationship(back_populates="buy_x_get_y")
