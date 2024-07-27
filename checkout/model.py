from enum import Enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from user_address.model import UserAddress
    from customer.model import Customer
    from cart.model import Cart
    from invoice.model import Invoice
    from price.model import Price
    from lib.many_to_many_tables import CheckoutDiscountLinks


class CheckoutStatusEnum(str, Enum):
    OPEN = "open"
    ABANDONED = "abandoned"
    COMPLETE = "complete"
    EXPIRED = "expired"


class CheckoutPaymentStatus(str, Enum):
    PAID = "paid"
    UNPAID = "unpaid"


class Checkout(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("ch"))
    status: CheckoutStatusEnum = Field(default=CheckoutStatusEnum.OPEN)
    payment_status: CheckoutPaymentStatus = Field(default=CheckoutPaymentStatus.UNPAID)
    return_url: str = Field(nullable=True)
    success_url: str = Field(nullable=True)
    url: str = Field(nullable=True)
    amount_total: int = Field()
    amount_subtotal: int = Field()
    amount_discount: int = Field()
    amount_shipping: int = Field()
    amount_tax: int = Field()
    expires_at: int = Field()

    # Do not use cart for getting line items.
    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="checkouts")
    cart_id: str = Field(foreign_key="cart.id")
    cart: "Cart" = Relationship(back_populates="checkouts")
    customer_id: str = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="checkouts")
    customer_address_id: str = Field(foreign_key="user_address.id", nullable=True)
    customer_address: "UserAddress" = Relationship(back_populates="checkouts")
    invoice: "Invoice" = Relationship(back_populates="checkout")
    # payment_intent_id: str = Field(foreign_key="payment_intent.id")
    # payment_intent:"PaymentIntent" = Relationship( back_populates="checkout")
    # order_id: str = Field(foreign_key="order.id", nullable=True)
    # order :"Order"= Relationship( back_populates="checkout")

    line_items: list["CheckoutLineItem"] = Relationship(
        back_populates="checkout",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    discount_links: list["CheckoutDiscountLinks"] = Relationship(
        back_populates="checkout",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class CheckoutLineItem(SqlBase, table=True):
    __tablename__ = "_checkout_line_item"

    id: str = Field(primary_key=True, default_factory=get_primary_key("_cli"))
    quantity: int = Field()

    checkout_id: str = Field(foreign_key="checkout.id")
    checkout: "Checkout" = Relationship(back_populates="line_items")
    price_id: str = Field(foreign_key="price.id")
    price: "Price" = Relationship(back_populates="checkout_line_items")
