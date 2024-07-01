from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from product.model import Product


class Option(SqlBase, table=True):
    id: str = Field(primary_key=True, default=get_primary_key("opt"))
    name: str = Field()
    # TODO add values when using postgres
    values: list[str] = Field()

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="options")
    product_id: str = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="options")
