from typing import TYPE_CHECKING
from sqlmodel import (
    Field,
    Relationship,
    UniqueConstraint,
    ARRAY,
    VARCHAR,
    Column,
    ForeignKey,
    Text,
)


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from option.model import Option
    from variant.model import Variant
    from discount.model import DiscountConfigOffProduct, DiscountConfigBuyXGetY
    from review.model import Review
    from lib.many_to_many_tables import CollectionProductLink


class Product(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("prod"))
    name: str = Field()
    description: str = Field(nullable=True)
    handle: str = Field()
    active: bool = Field()
    images: list[str] = Field(sa_column=Column(ARRAY(Text), nullable=True))
    shippable: bool = Field(default=True)
    preorder: bool = Field(default=False)
    rating: int = Field(nullable=True)  # Range from 0 to 50

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="products")
    options: list["Option"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    variants: list["Variant"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    collection_links: list["CollectionProductLink"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    reviews: list["Review"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    discount_config_off_product_id: str = Field(
        sa_column=Column(
            VARCHAR,
            ForeignKey("_discount_config_off_product.id", use_alter=True),
            nullable=True,
        )
    )
    discount_config_off_product: "DiscountConfigOffProduct" = Relationship(
        back_populates="products",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    discount_config_buy_x_get_y_id: str = Field(
        sa_column=Column(
            VARCHAR,
            ForeignKey("_discount_config_buy_x_get_y.id", use_alter=True),
            nullable=True,
        )
    )
    discount_config_buy_x_get_y: "DiscountConfigBuyXGetY" = Relationship(
        back_populates="products_buy"
    )

    __table_args__ = (
        UniqueConstraint("shop_id", "handle", name="unique_product_handle_shop"),
    )
