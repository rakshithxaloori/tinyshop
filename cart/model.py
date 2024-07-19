import enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from cart_item.model import CartItem
    from discount.model import Discount
    from checkout.model import Checkout


class CartStatusEnum(str, enum.Enum):
    REQUIRES_PAYMENT = "requires_payment"
    ABANDONED = "abandoned"
    PAID = "paid"


class Cart(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("cart"))
    status: CartStatusEnum = Field(default=CartStatusEnum.REQUIRES_PAYMENT)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="carts")
    items: list["CartItem"] = Relationship(
        back_populates="cart",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    # TODO
    # discounts: list["Discount"] = Relationship(back_populates="carts")
    checkouts: list["Checkout"] = Relationship(back_populates="cart")
    # order_id = Field(Text, ForeignKey("order.id"))
    # order = relationship("Order", back_populates="cart")
    # customer
