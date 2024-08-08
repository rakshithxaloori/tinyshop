from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.cart.model import Cart
    from app.price.model import Price


class CartItem(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("ci"))
    quantity: int = Field()

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="cart_items")
    cart_id: str = Field(foreign_key="cart.id")
    cart: "Cart" = Relationship(back_populates="items")
    price_id: str = Field(foreign_key="price.id")
    price: "Price" = Relationship(back_populates="cart_items")

    # TODO cart_id, price_id have to be unique
