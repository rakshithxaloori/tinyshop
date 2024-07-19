from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key
from price.enum import PriceTypeEnum, RecurringTypeEnum

if TYPE_CHECKING:
    from shop.model import Shop
    from variant.model import Variant
    from cart.model import CartItem
    from subscription.model import Subscription
    from order.model import OrderLineItem
    from checkout.model import CheckoutLineItem


class Price(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("price"))
    active: bool = Field()
    currency: str = Field(max_length=3)
    type: PriceTypeEnum = Field()
    unit_amount: int = Field()
    unit_compare_amount: int = Field(nullable=True)
    is_default: bool = Field(default=False)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="prices")
    variant_id: str = Field(foreign_key="variant.id")
    variant: "Variant" = Relationship(back_populates="prices")

    recurring: "Recurring" = Relationship(
        back_populates="price",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    customer_unit_amount: "CustomerUnitAmount" = Relationship(
        back_populates="price",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    cart_items: list["CartItem"] = Relationship(
        back_populates="price",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    subscriptions: list["Subscription"] = Relationship(
        back_populates="price",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    checkout_line_items: list["CheckoutLineItem"] = Relationship(back_populates="price")
    order_line_items: list["OrderLineItem"] = Relationship(back_populates="price")


class CustomerUnitAmount(SqlBase, table=True):
    __tablename__ = "_customer_unit_amount"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_cua"))
    maximum: int = Field(nullable=True)
    minimum: int = Field(nullable=True)
    preset: int = Field(default=1)

    price_id: str = Field(foreign_key="price.id", unique=True)
    price: "Price" = Relationship(back_populates="customer_unit_amount")


class Recurring(SqlBase, table=True):
    __tablename__ = "_recurring"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_recur"))
    interval: RecurringTypeEnum = Field()
    interval_count: int = Field()

    price_id: str = Field(foreign_key="price.id", unique=True)
    price: "Price" = Relationship(back_populates="recurring")
