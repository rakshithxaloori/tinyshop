from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.inventory.model import Inventory


class Warehouse(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("ware"))
    name: str = Field()
    active: bool = Field()
    phone: str = Field(nullable=True)

    # Warehouse Address
    line1: str = Field()
    line2: str = Field(nullable=True)
    city: str = Field()
    state: str = Field()
    country: str = Field(max_length=2)
    postal_code: str = Field()

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="warehouses")
    inventories: list["Inventory"] = Relationship(back_populates="warehouse")
    # shippings = relationship("Shipping", back_populates="warehouse")
