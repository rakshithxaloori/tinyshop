from cart.cart_item.model import CartItem
from cart.cart_item import schema


def pydantify_cart_items(rows: list[CartItem]) -> list[schema.CartItem]:
    cart_items: list[schema.CartItem] = []
    for ci in rows:
        cart_items.append(
            schema.CartItem(
                **ci.model_dump(exclude={"created", "updated"}),
                created=int(ci.created.timestamp()),
                updated=int(ci.updated.timestamp()),
            )
        )
    return cart_items
