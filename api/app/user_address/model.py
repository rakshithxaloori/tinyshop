from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from app.user.model import User
    from app.checkout.model import Checkout
    from app.subscription.model import Subscription


class UserAddress(SqlBase, table=True):
    __tablename__ = "user_address"

    id: str = Field(primary_key=True, default_factory=get_primary_key("addr"))
    name: str = Field()
    line1: str = Field()
    line2: str = Field(nullable=True)
    city: str = Field()
    state: str = Field()
    country: str = Field(max_length=2)
    postal_code: str = Field()

    user_id: str = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="addresses")
    checkouts: list["Checkout"] = Relationship(back_populates="customer_address")
    subscriptions: list["Subscription"] = Relationship(
        back_populates="customer_address",
        sa_relationship_kwargs={"cascade": "delete"},
    )
