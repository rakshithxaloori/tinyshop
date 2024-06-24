import enum
from sqlalchemy import Column, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship


from utils.base import Base
from utils.primary_key import get_primary_key


class Team(Base):
    __tablename__ = "team"

    id = Column(Text, primary_key=True, default=get_primary_key("team"))
    name = Column(Text)

    shops = relationship("Shop", back_populates="team")
    keys = relationship("Keys", back_populates="team")


class AccessScopeEnum(enum.Enum):
    owner = "owner"
    admin = "admin"


class Keys(Base):
    __tablename__ = "keys"

    id = Column(Text, primary_key=True, default=get_primary_key("keys"))
    name = Column(Text)
    livemode = Column(Boolean)
    hashed_key = Column(Text)
    access_scope = Column(Enum(AccessScopeEnum))

    team_id = Column(Text, ForeignKey("team.id", ondelete="CASCADE"))
    team = relationship("Team", back_populates="keys")
