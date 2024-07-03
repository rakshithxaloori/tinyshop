from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from cart.model import Cart
    from product.price.model import Price


class CartItem(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("ci"))
    quantity: int = Field()

    cart_id: str = Field(foreign_key="cart.id")
    cart: "Cart" = Relationship(back_populates="items")
    price_id: str = Field(foreign_key="price.id")
    price: "Price" = Relationship(back_populates="cart_items")
