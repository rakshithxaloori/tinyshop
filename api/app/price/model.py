from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key
from app.price.enum import PriceTypeEnum, RecurringTypeEnum

if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.variant.model import Variant
    from app.cart.model import CartItem

    from app.subscription.model import SubscriptionLineItem
    from app.order.model import OrderLineItem
    from app.checkout.model import CheckoutLineItem
    from app.invoice.model import InvoiceLineItem


class Price(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("price"))
    active: bool = Field()
    currency: str = Field(max_length=3)
    type: PriceTypeEnum = Field()
    unit_amount: int = Field()
    unit_compare_amount: int = Field(nullable=True)
    is_default: bool = Field(default=False)

    # Customer Unit Amount
    maximum: int = Field(nullable=True)
    minimum: int = Field(nullable=True)
    preset: int = Field(default=1)

    # Recurring
    interval: RecurringTypeEnum = Field(nullable=True)
    interval_count: int = Field(nullable=True)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="prices")
    variant_id: str = Field(foreign_key="variant.id")
    variant: "Variant" = Relationship(back_populates="prices")

    cart_items: list["CartItem"] = Relationship(
        back_populates="price",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    subscription_line_items: list["SubscriptionLineItem"] = Relationship(
        back_populates="price",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    checkout_line_items: list["CheckoutLineItem"] = Relationship(back_populates="price")
    invoice_line_items: list["InvoiceLineItem"] = Relationship(back_populates="price")
    order_line_items: list["OrderLineItem"] = Relationship(back_populates="price")
