from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.user.model import User
    from app.review.model import Review
    from app.lib.many_to_many_tables import DiscountCustomerLink

    from app.subscription.model import Subscription
    from app.checkout.model import Checkout
    from app.invoice.model import Invoice
    from app.order.model import Order


class Customer(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("cus"))
    otp: str = Field(nullable=True)
    expires_at: int = Field(nullable=True)
    is_verified: bool = Field(default=False)

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
