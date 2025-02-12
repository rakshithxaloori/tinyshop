import enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.cart_item.model import CartItem
    from app.checkout.model import Checkout
    from app.lib.many_to_many_tables import CartDiscountLinks


class CartStatusEnum(str, enum.Enum):
    REQUIRES_PAYMENT = "requires_payment"
    ABANDONED = "abandoned"
    PAID = "paid"


class Cart(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("cart"))
    status: CartStatusEnum = Field(default=CartStatusEnum.REQUIRES_PAYMENT)
    currency: str = Field(max_length=3)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="carts")
    items: list["CartItem"] = Relationship(
        back_populates="cart",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    # TODO
    discount_links: list["CartDiscountLinks"] = Relationship(
        back_populates="cart",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    checkouts: list["Checkout"] = Relationship(back_populates="cart")
    # order_id = Field(Text, ForeignKey("order.id"))
    # order = relationship("Order", back_populates="cart")
    # customer
