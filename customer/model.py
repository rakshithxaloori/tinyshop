from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from user.model import User
    from review.model import Review
    from lib.many_to_many_tables import DiscountCustomerLink

    from subscription.model import Subscription
    from checkout.model import Checkout
    from invoice.model import Invoice
    from order.model import Order


class Customer(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("cus"))
    user_id: str = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="customers")
    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="customers")

    reviews: list["Review"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    discount_links: list["DiscountCustomerLink"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    checkouts: list["Checkout"] = Relationship(back_populates="customer")
    subscriptions: list["Subscription"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    invoices: list["Invoice"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    orders: list["Order"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "delete"},
    )

    # TODO unique, shop id, user id
