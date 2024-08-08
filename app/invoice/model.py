import enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key
from app.lib.enum import PaymentsProviderEnum


if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.customer.model import Customer
    from app.checkout.model import Checkout
    from app.subscription.model import Subscription
    from app.order.model import Order
    from app.price.model import Price


class InvoiceStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    UNCOLLECTIBLE = "uncollectible"
    VOID = "void"


class Invoice(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("in"))
    amount_paid: int = Field()
    amount_remaining: int = Field()
    amount_shipping: int = Field()
    amount_tax: int = Field()
    amount_subtotal: int = Field()
    amount_total: int = Field()
    amount_discount: int = Field()
    attempt_count: int = Field(default=0)
    currency: str = Field(max_length=3)
    attempted: bool = Field(default=False)
    status: InvoiceStatusEnum = Field()
    due_date: int = Field(nullable=True)
    invoice_pdf: str = Field(nullable=True)
    paid: bool = Field()

    provider: PaymentsProviderEnum = Field()

    # Razorpay
    razorpay_order_id: str = Field(nullable=True)

    line_items: list["InvoiceLineItem"] = Relationship(
        back_populates="invoice",
        sa_relationship_kwargs={"cascade": "delete"},
    )

    # Customer Address
    line1: str = Field()
    line2: str = Field(nullable=True)
    city: str = Field()
    state: str = Field()
    country: str = Field(max_length=2)
    postal_code: str = Field()

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="invoices")
    customer_id: str = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="invoices")
    checkout_id: str = Field(foreign_key="checkout.id", nullable=True)
    checkout: "Checkout" = Relationship(back_populates="invoices")
    subscription_id: str = Field(foreign_key="subscription.id", nullable=True)
    subscription: "Subscription" = Relationship(back_populates="invoices")
    order: "Order" = Relationship(back_populates="invoice")
    # TODO list[payment intent]


class InvoiceLineItem(SqlBase, table=True):
    __tablename__ = "_invoice_line_item"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_ili"))
    quantity: int = Field()
    unit_amount: int = Field()

    invoice_id: str = Field(foreign_key="invoice.id")
    invoice: "Invoice" = Relationship(back_populates="line_items")
    price_id: str = Field(foreign_key="price.id")
    price: "Price" = Relationship(back_populates="invoice_line_items")
