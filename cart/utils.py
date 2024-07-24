from cart.model import Cart
from cart import schema
from cart_item import schema as ci_schema
from cart_item.model import CartItem


def pydantify_carts(rows: list[tuple[Cart, CartItem | None]]) -> list[schema.Cart]:
    carts_dict: dict[str, schema.Cart] = {}
    for cart, cart_item in rows:
        if cart.id not in carts_dict:
            carts_dict[cart.id] = schema.Cart(
                **cart.model_dump(),
                cart_items=ci_schema.CartItemList(
                    data=[],
                    has_more=False,  # TODO
                    url=f"/v1/carts/{cart.id}/cart_items",
                ),
            )
        if cart_item:
            carts_dict[cart.id].cart_items.data.append(
                ci_schema.CartItem(
                    **cart_item.model_dump(exclude={"price"}),
                    price=cart_item.price_id,  # TODO
                )
            )

    return list(carts_dict.values())
