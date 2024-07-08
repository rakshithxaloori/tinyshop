from typing import Annotated
from fastapi import Form


from discount import schema


def create_discount_form(
    config_off_product_quantity_min: Annotated[int | None, Form()] = None,
    config_off_product_amount_off: Annotated[int | None, Form()] = None,
    customers: Annotated[list(str) | None, Form()] = None,
):
    pass
