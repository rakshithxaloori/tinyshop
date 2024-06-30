from sqlalchemy import Column, Text, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class Warehouse(SqlBase):
    __tablename__ = "warehouse"

    id = Column(Text, primary_key=True, default=get_primary_key("ware"))
    name = Column(Text)
    active = Column(Boolean)
    phone = Column(Text, nullable=True)

    shop_id = Column(Text, ForeignKey("shop.id", ondelete="CASCADE"))
    shop = relationship("Shop", back_populates="warehouses")
    address_id = Column(Text, ForeignKey("_warehouse_address.id"))
    address = relationship("WarehouseAddress", back_populates="warehouse")
    inventories = relationship("Inventory", back_populates="warehouse")
    shippings = relationship("Shipping", back_populates="warehouse")


class WarehouseAddress(SqlBase):
    __tablename__ = "_warehouse_address"

    id = Column(Text, primary_key=True, default=get_primary_key("_waddr"))
    line1 = Column(Text)
    line2 = Column(Text, nullable=True)
    city = Column(Text)
    state = Column(Text)
    country = Column(String(2))
    postal_code = Column(Text)

    warehouse_id = Column(Text, ForeignKey("warehouse.id", ondelete="CASCADE"))
    warehouse = relationship("Warehouse", back_populates="address")
