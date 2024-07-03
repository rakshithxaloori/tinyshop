from cart.model import Cart
from cart import schema
from cart.cart_item import schema as ci_schema
from cart.cart_item.model import CartItem


def pydantify_carts(rows: list[tuple[Cart, CartItem | None]]) -> list[schema.Cart]:
    carts_dict: dict[str, schema.Cart] = {}
    for cart, cart_item in rows:
        if cart.id not in carts_dict:
            carts_dict[cart.id] = schema.Cart(
                **cart.model_dump(exclude={"created", "updated"}),
                created=int(cart.created.timestamp()),
                updated=int(cart.updated.timestamp()),
                cart_items=ci_schema.CartItemList(
                    data=[],
                    has_more=False,  # TODO
                    url="/v1/carts/{cart_id}/cart_items".format(cart_id=cart.id),
                ),
            )
        if cart_item:
            carts_dict[cart.id].cart_items.data.append(
                ci_schema.CartItem(
                    **cart_item.model_dump(exclude={"created", "updated"}),
                    created=int(cart_item.created.timestamp()),
                    updated=int(cart_item.updated.timestamp()),
                )
            )

    return list(carts_dict.values())
