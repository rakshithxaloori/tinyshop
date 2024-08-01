from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key
from lib.enum import PaymentsProviderEnum


if TYPE_CHECKING:
    from customer.model import Customer

    from product.model import Product
    from option.model import Option
    from variant.model import Variant
    from price.model import Price
    from collection.model import Collection

    from warehouse.model import Warehouse
    from inventory.model import Inventory

    from cart.model import Cart
    from cart_item.model import CartItem

    from review.model import Review
    from discount.model import Discount

    from checkout.model import Checkout
    from subscription.model import Subscription
    from invoice.model import Invoice
    from order.model import Order


class Shop(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("shop"))
    name: str = Field(nullable=True)

    default_payments_provider: PaymentsProviderEnum = Field(nullable=True)

    # Payment Providers
    razorpay_key_id: str = Field(nullable=True)
    razorpay_key_secret: str = Field(nullable=True)
    razorpay_plans: list["RazorpayPlan"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )

    secret_keys: list["SecretKey"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )

    customers: list["Customer"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    products: list["Product"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    options: list["Option"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    variants: list["Variant"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    prices: list["Price"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    collections: list["Collection"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    warehouses: list["Warehouse"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    inventories: list["Inventory"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    carts: list["Cart"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    cart_items: list["CartItem"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    reviews: list["Review"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    discounts: list["Discount"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    checkouts: list["Checkout"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    subscriptions: list["Subscription"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    invoices: list["Invoice"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    orders: list["Order"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class SecretKey(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("key"))
    secret_key: str = Field()

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="secret_keys")


from price.enum import RecurringTypeEnum


class RazorpayPlan(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("rzpy_plan"))

    # ID of the Plan in Razorpay
    ext_id: str = Field()
    interval: RecurringTypeEnum = Field()
    interval_count: int = Field(default=1)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="razorpay_plans")

    # Notes
    # Every Razorpay is created with 100 amount(1 INR)
    # All subscription items are added as add-ons

    # TODO shop_id, inteval are unique
