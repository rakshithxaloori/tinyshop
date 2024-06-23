from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship


from utils.base import SqlBase
from utils.primary_key import get_primary_key


class Shop(SqlBase):
    __tablename__ = "shops"

    id = Column(Text, primary_key=True, default=get_primary_key("shop"))
    name = Column(Text, nullable=True)

    team_id = Column(Text, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="shops")
    customers = relationship("Customer", back_populates="shop")
