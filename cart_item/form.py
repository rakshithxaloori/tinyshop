from typing import Annotated
from fastapi import Form


from cart_item import schema


def create_cart_item_form(
    cart: Annotated[str, Form()],
    price: Annotated[str, Form()],
    quantity: Annotated[int, Form()] = 1,
) -> schema.CartItemCreate:
    return schema.CartItemCreate(
        cart=cart,
        price=price,
        quantity=quantity,
    )


def update_cart_item_form(
    quantity: Annotated[int, Form()],
) -> schema.CartItemUpdate:
    return schema.CartItemUpdate(quantity=quantity)
