import enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from customer.model import Customer
    from checkout.model import Checkout
    from cart.model import Cart
    from order.model import Order


class InvoiceStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    UNCOLLECTIBLE = "uncollectible"
    VOID = "void"


class Invoice(SqlBase, table=True):
    __tablename__ = "invoice"

    id: str = Field(primary_key=True, default_factory=get_primary_key("in"))
    amount_due: int = Field()
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
    customer_email: str = Field(nullable=True)
    customer_phone: str = Field()
    customer_name: str = Field()
    due_date: int = Field(nullable=True)
    invoice_pdf: str = Field(nullable=True)
    paid: bool = Field()

    # charge TODO
    customer_id: str = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="invoices")
    checkout_id: str = Field(foreign_key="checkout.id", nullable=True)
    checkout: "Checkout" = Relationship(back_populates="invoice")
    order: "Order" = Relationship(back_populates="invoice")
    # TODO subscription invoice link table
    # subscriptions:list["Subscription"] = Relationship( back_populates="invoices")
    customer_address: "InvoiceCustomerAddress" = Relationship(back_populates="invoice")
    # TODO list[payment intent]


# TODO invoice lines


class InvoiceCustomerAddress(SqlBase, table=True):
    __tablename__ = "_invoice_customer_address"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_ica"))
    line1: str = Field()
    line2: str = Field(nullable=True)
    city: str = Field()
    state: str = Field()
    country: str = Field(max_length=2)
    postal_code: str = Field()

    invoice_id: str = Field(foreign_key="invoice.id")
    invoice: "Invoice" = Relationship(back_populates="customer_address")
