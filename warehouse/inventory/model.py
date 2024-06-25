from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class Inventory(SqlBase):
    __tablename__ = "inventory"

    id = Column(Text, primary_key=True, default=get_primary_key("inv"))
    quantity = Column(Integer)

    variant_id = Column(Text, ForeignKey("variant.id", ondelete="CASCADE"))
    variant = relationship("Variant", back_populates="inventories")
    warehouse_id = Column(Text, ForeignKey("warehouse.id", ondelete="CASCADE"))
    warehouse = relationship("Warehouse", back_populates="inventories")
