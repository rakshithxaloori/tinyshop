from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from lib.many_to_many_tables import CollectionProductLink


class Collection(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("col"))
    name: str = Field()
    image_web: str = Field(nullable=True)
    image_mobile: str = Field(nullable=True)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="collections")
    product_links: list["CollectionProductLink"] = Relationship(
        back_populates="collection",
        sa_relationship_kwargs={"cascade": "delete"},
    )
