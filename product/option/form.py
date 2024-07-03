from typing import Annotated
from fastapi import Form


from product.option import schema


def create_option_form(
    name: Annotated[str, Form()],
    values: Annotated[list[str], Form(alias="values[]")],
):
    return schema.OptionCreate(
        name=name,
        values=values,
    )


def update_option_form(
    name: Annotated[str | None, Form()] = None,
    values: Annotated[list[str], Form(alias="values[]")] = None,
):
    return schema.OptionUpdate(
        name=name,
        values=values,
    )
