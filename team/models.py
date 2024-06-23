from sqlalchemy import Column, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship


from utils.base import Base
from utils.primary_key import get_primary_key


class Team(Base):
    __tablename__ = "teams"

    id = Column(Text, primary_key=True, default=get_primary_key("team"))
    name = Column(Text)

    shops = relationship("Shop", back_populates="team")


class AccessScopeEnum(Enum):
    owner = "owner"
    admin = "admin"


class Keys(Base):
    __tablename__ = "keys"

    id = Column(Text, primary_key=True, default=get_primary_key("keys"))
    name = Column(Text)
    hashed_test_key = Column(Text)
    hashed_live_key = Column(Text)
    access_scope = Column(Enum(AccessScopeEnum))

    team_id = Column(Text, ForeignKey("teams.id", ondelete="CASCADE"))
    team = relationship("Team", back_populates="keys")
