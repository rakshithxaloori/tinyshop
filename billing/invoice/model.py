import enum
from sqlalchemy import (
    Column,
    Text,
    ForeignKey,
    Boolean,
    Integer,
    String,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class InvoiceStatusEnum(enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    UNCOLLECTIBLE = "uncollectible"
    VOID = "void"


class Invoice(SqlBase):
    __tablename__ = "invoice"

    id = Column(Text, primary_key=True, default=get_primary_key("in"))
    amount_due = Column(Integer)
    amount_paid = Column(Integer)
    amount_remaining = Column(Integer)
    amount_shipping = Column(Integer)
    amount_tax = Column(Integer)
    amount_subtotal = Column(Integer)
    amount_total = Column(Integer)
    amount_discount = Column(Integer)
    attempt_count = Column(Integer, default=0)
    currency = Column(String(3))
    attempted = Column(Boolean, default=False)
    status = Column(Enum(InvoiceStatusEnum))
    customer_email = Column(Text, nullable=True)
    customer_phone = Column(Text)
    customer_name = Column(Text)
    due_date = Column(DateTime, nullable=True)
    invoice_pdf = Column(Text, nullable=True)
    paid = Column(Boolean)

    # charge TODO
    customer_id = Column(Text, ForeignKey("customer.id", ondelete="CASCADE"))
    customer = relationship("Customer", back_populates="invoices")
    checkout_id = Column(Text, ForeignKey("checkout.id"), nullable=True)
    checkout = relationship("Checkout", back_populates="invoice")
    cart_id = Column(Text, ForeignKey("cart.id", ondelete="CASCADE"))
    cart = relationship("Cart", back_populates="invoice")
    order_id = Column(Text, ForeignKey("order.id"), nullable=True)
    order = relationship("Order", back_populates="invoice")
    subscriptions = relationship("Subscriptions", back_populates="invoices")
    customer_address_id = Column(Text, ForeignKey("_invoice_customer_address.id"))
    customer_address = relationship("InvoiceCustomerAddress", back_populates="invoice")


class InvoiceCustomerAddress(SqlBase):
    __tablename__ = "_invoice_customer_address"

    id = Column(Text, primary_key=True, default=get_primary_key("_ica"))
    line1 = Column(Text)
    line2 = Column(Text, nullable=True)
    city = Column(Text)
    state = Column(Text)
    country = Column(String(2))
    postal_code = Column(Text)

    invoice_id = Column(Text, ForeignKey("invoice.id", ondelete="CASCADE"))
    invoice = relationship("Invoice", back_populates="customer_address")
