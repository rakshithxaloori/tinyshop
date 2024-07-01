from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


if TYPE_CHECKING:
    from team.model import Team
    from customer.model import Customer
    from customer.address.model import CustomerAddress
    from product.model import Product


class Shop(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("shop"))
    name: str = Field(nullable=True)

    team_id: str = Field(foreign_key="team.id", unique=True)
    team: "Team" = Relationship(back_populates="shop")
    customers: list["Customer"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    customer_addresses: list["CustomerAddress"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    products: list["Product"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
