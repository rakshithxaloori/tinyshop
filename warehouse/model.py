from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop


class Warehouse(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("ware"))
    name: str = Field()
    active: bool = Field()
    phone: str = Field(nullable=True)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="warehouses")
    address: "WarehouseAddress" = Relationship(
        back_populates="warehouse",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    # inventories = relationship("Inventory", back_populates="warehouse")
    # shippings = relationship("Shipping", back_populates="warehouse")


class WarehouseAddress(SqlBase):
    __tablename__ = "_warehouse_address"

    id: str = Field(primary_key=True, default=get_primary_key("_waddr"))
    line1: str = Field()
    line2: str = Field(nullable=True)
    city: str = Field()
    state: str = Field()
    country: str = Field(max_length=2)
    postal_code: str = Field()

    warehouse_id: str = Field(foreign_key="warehouse.id")
    warehouse: "Warehouse" = Relationship(back_populates="address")
