from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.variant.model import Variant
    from app.warehouse.model import Warehouse


class Inventory(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("inv"))
    quantity: int = Field()

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="inventories")
    variant_id: str = Field(foreign_key="variant.id")
    variant: "Variant" = Relationship(back_populates="inventories")
    warehouse_id: str = Field(foreign_key="warehouse.id")
    warehouse: "Warehouse" = Relationship(back_populates="inventories")

    __table_args__ = (
        UniqueConstraint("variant_id", "warehouse_id", name="unique_variant_warehouse"),
    )
