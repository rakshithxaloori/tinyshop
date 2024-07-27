from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from customer.model import Customer
    from user_address.model import UserAddress


class User(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("user"))
    name: str = Field(nullable=True)
    email: str = Field(nullable=True)  # TODO unique=True?
    phone: str = Field(unique=True)

    customers: list["Customer"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    addresses: list["UserAddress"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "delete"},
    )
