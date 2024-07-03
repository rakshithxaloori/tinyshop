import enum
from sqlalchemy import Column, Text, ForeignKey, Enum, String, Integer, DateTime
from sqlalchemy.orm import relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


class CheckoutStatusEnum(str, enum.Enum):
    OPEN = "open"
    COMPLETE = "complete"
    EXPIRED = "expired"


class CheckoutPaymentStatus(str, enum.Enum):
    PAID = "paid"
    UNPAID = "unpaid"


class Checkout(SqlBase):
    __tablename__ = "checkout"

    id = Column(Text, primary_key=True, default_factory=get_primary_key("co"))
    customer_email = Column(Text, nullable=True)
    customer_phone = Column(Text)
    status = Column(Enum(CheckoutStatusEnum))
    currency = Column(String(3))
    payment_status = Column(Enum(CheckoutPaymentStatus))
    return_url = Column(Text, nullable=True)
    success_url = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    amount_total = Column(Integer)
    amount_subtotal = Column(Integer)
    amount_discount = Column(Integer)
    amount_shipping = Column(Integer)
    amount_tax = Column(Integer)
    expires_at = Column(DateTime)

    cart_id = Column(Text, ForeignKey("cart.id"))
    cart = relationship("Cart", back_populates="checkouts")
    customer_id = Column(Text, ForeignKey("customer.id"), nullable=True)
    customer = relationship("Customer", back_populates="checkouts")
    invoice_id = Column(Text, ForeignKey("invoice.id"), nullable=True)
    invoice = relationship("Invoice", back_populates="checkout")
    payment_intent_id = Column(Text, ForeignKey("payment_intent.id"))
    payment_intent = relationship("PaymentIntent", back_populates="checkout")
    order_id = Column(Text, ForeignKey("order.id"), nullable=True)
    order = relationship("Order", back_populates="checkout")
    customer_details_id = Column(
        Text, ForeignKey("_checkout_customer_details.id"), nullable=True
    )
    customer_details = relationship(
        "_CheckoutCustomerDetails", back_populates="checkout"
    )
    shipping_address_id = Column(
        Text, ForeignKey("_checkout_shipping_address.id"), nullable=True
    )
    shipping_address = relationship(
        "CheckoutShippingAddress", back_populates="checkout"
    )


class CheckoutCustomerDetails(SqlBase):
    __tablename__ = "_checkout_customer_details"

    id = Column(Text, primary_key=True, default_factory=get_primary_key("_ccd"))
    email = Column(Text, nullable=True)
    name = Column(Text)
    phone = Column(Text)

    address_id = Column(
        Text, ForeignKey("_checkout_customer_details_address.id"), nullable=True
    )
    address = relationship(
        "CheckoutCustomerDetailsAddress", back_populates="customer_details"
    )
    checkout_id = Column(Text, ForeignKey("checkout.id", ondelete="CASCADE"))


class CheckoutCustomerDetailsAddress(SqlBase):
    __tablename__ = "_checkout_customer_details_address"

    id = Column(Text, primary_key=True, default_factory=get_primary_key("_ccdaddr"))
    name = Column(Text)
    line1 = Column(Text)
    line2 = Column(Text, nullable=True)
    city = Column(Text)
    state = Column(Text)
    country = Column(String(2))
    postal_code = Column(Text)

    customer_details_id = Column(
        Text, ForeignKey("_checkout_customer_details.id", ondelete="CASCADE")
    )


class CheckoutShippingAddress(SqlBase):
    __tablename__ = "_checkout_shipping_address"

    id = Column(Text, primary_key=True, default_factory=get_primary_key("_c"))
    name = Column(Text)
    line1 = Column(Text)
    line2 = Column(Text, nullable=True)
    city = Column(Text)
    state = Column(Text)
    country = Column(String(2))
    postal_code = Column(Text)

    checkout_id = Column(Text, ForeignKey("checkout.id", ondelete="CASCADE"))
