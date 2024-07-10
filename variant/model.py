from typing import TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from product.model import Product
    from price.model import Price
    from inventory.model import Inventory
    from discount.model import DiscountConfigBuyXGetY


class Variant(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("var"))
    name: str = Field()
    description: str = Field(nullable=True)
    active: bool = Field()
    options: str = Field(nullable=True)
    accept_zero_inventory_orders: bool = Field(default=False)
    next_refill: datetime = Field(nullable=True)
    unit_label: str = Field(nullable=True)
    is_default: bool = Field(default=False, nullable=True)  # TODO remove nullable=True

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="variants")
    product_id: str = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="variants")
    prices: list["Price"] = Relationship(
        back_populates="variant",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    package_dimensions: "PackageDimensions" = Relationship(
        back_populates="variant",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    inventories: list["Inventory"] = Relationship(
        back_populates="variant",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    # subscriptions = relationship("Subscription", back_populates="variant")
    # shipping_lines = relationship("ShippingLines", back_populates="variant")
    discount_config_buy_x_get_y: list["DiscountConfigBuyXGetY"] = Relationship(
        back_populates="variant_get",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class PackageDimensions(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("_pdim"))
    height: float = Field()
    width: float = Field()
    length: float = Field()
    weight: float = Field()

    variant_id: str = Field(foreign_key="variant.id", unique=True)
    variant: "Variant" = Relationship(back_populates="package_dimensions")
