from typing import Annotated
from fastapi import Form


from checkout import schema


def create_checkout_form(
    customer: Annotated[str, Form()],
    cart: Annotated[str, Form()],
    return_url: Annotated[str, Form()],
    success_url: Annotated[str, Form()],
    url: Annotated[str, Form()],
    customer_address: Annotated[str | None, Form()] = None,
) -> schema.CheckoutCreate:
    return schema.CheckoutCreate(
        customer=customer,
        customer_address=customer_address,
        cart=cart,
        return_url=return_url,
        success_url=success_url,
        url=url,
    )


def update_checkout_form(
    customer_address: Annotated[str, Form()],
) -> schema.CheckoutUpdate:
    return schema.CheckoutUpdate(customer_address=customer_address)
