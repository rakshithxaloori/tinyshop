from typing import Annotated
from fastapi import Form


from cart import schema


def create_cart_form(
    price: Annotated[str | None, Form(alias="cart_item[price]")] = None,
    quantity: Annotated[int | None, Form(alias="cart_item[quantity]")] = None,
) -> schema.CartCreate:
    return schema.CartCreate(
        cart_item=(
            schema.CartItemCreate(
                price=price,
                quantity=quantity,
            )
            if price and quantity
            else None
        )
    )


def update_cart_form(
    status: Annotated[str, Form()],
) -> schema.CartUpdate:
    return schema.CartUpdate(
        status=status,
    )
