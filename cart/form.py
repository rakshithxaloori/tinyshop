from typing import Annotated
from fastapi import Form


from cart import schema


def create_cart_form(
    price: Annotated[str, Form()],
    quantity: Annotated[int, Form()] = 1,
) -> schema.CartCreate:
    return schema.CartCreate(
        cart_item=schema.CartItemCreate(
            price=price,
            quantity=quantity,
        )
    )


def update_cart_form(
    status: Annotated[str, Form()],
) -> schema.CartUpdate:
    return schema.CartUpdate(status=status)
