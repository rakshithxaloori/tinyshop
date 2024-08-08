from app.cart.model import Cart
from app.cart import schema
from app.cart_item import schema as ci_schema
from app.discount import schema as dis_schema
from app.lib.limit import LIST_LIMIT_COUNT
from app.cart_item.utils import pydantify_cart_items


def pydantify_carts(rows: list[Cart]) -> list[schema.Cart]:
    carts_dict: dict[str, schema.Cart] = {}
    for cart in rows:
        if cart.id not in carts_dict:
            carts_dict[cart.id] = schema.Cart(
                **cart.model_dump(),
                cart_items=ci_schema.CartItemList(
                    data=pydantify_cart_items(cart.items[:LIST_LIMIT_COUNT]),
                    has_more=False,  # TODO
                    url=f"/v1/carts/{cart.id}/cart_items",
                ),
                discounts=dis_schema.DiscountList(
                    url=f"/v1/discounts?cart={cart.id}",
                    data=[
                        cd_link.discount_id
                        for cd_link in cart.discount_links[:LIST_LIMIT_COUNT]
                    ],
                    has_more=False,  # TODO
                ),
            )

    return list(carts_dict.values())
