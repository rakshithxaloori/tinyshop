import enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop


class Team(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("team"))
    name: str = Field()

    shop: "Shop" = Relationship(back_populates="team")
    keys: list["Keys"] = Relationship(back_populates="team")


class AccessScopeEnum(str, enum.Enum):
    owner = "owner"
    admin = "admin"


class Keys(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("keys"))
    name: str = Field()
    livemode: bool = Field()
    hashed_key: str = Field()
    access_scope: AccessScopeEnum = Field()

    team_id: str = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="keys")
