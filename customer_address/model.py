from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from customer.model import Customer

    # from subscription.model import Subscription
    from checkout.model import Checkout


class CustomerAddress(SqlBase, table=True):
    __tablename__ = "customer_address"

    id: str = Field(primary_key=True, default_factory=get_primary_key("caddr"))
    name: str = Field()
    line1: str = Field()
    line2: str = Field(nullable=True)
    city: str = Field()
    state: str = Field()
    country: str = Field(max_length=2)
    postal_code: str = Field()

    customer_id: str = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="addresses")
    checkouts: list["Checkout"] = Relationship(
        back_populates="customer_address",
    )
    # subscriptions: list["Subscription"] = Relationship(
    #     back_populates="customer_address",
    #     sa_relationship_kwargs={"cascade": "delete"},
    # )
