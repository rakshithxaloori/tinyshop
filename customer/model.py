from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop


class Customer(SqlBase, table=True):
    __tablename__ = "customer"

    id: str = Field(primary_key=True, default_factory=get_primary_key("cus"))
    name: str = Field()
    email: str = Field(nullable=True)  # TODO unique=True?
    phone: str = Field(unique=True)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="customers")
    addresses: list["CustomerAddress"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    # checkouts = relationship("Checkout", back_populates="customer")
    # subscriptions = relationship("Subscription", back_populates="customer")
    # invoices = relationship("Invoice", back_populates="customer")
    # orders = relationship("Order", back_populates="customer")


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
    customer: Customer = Relationship(back_populates="addresses")
