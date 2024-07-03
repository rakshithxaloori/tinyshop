import re
import unicodedata
from typing import Annotated
from fastapi import Form


from product import schema


def get_handle(name: str) -> str:
    # Normalize the product name to NFKD form
    handle = unicodedata.normalize("NFKD", name)
    # Convert to lowercase
    handle = handle.lower()
    # Replace spaces and special characters with hyphens
    handle = re.sub(r"\s+", "-", handle)
    # Remove non-alphanumeric characters except for hyphens
    handle = re.sub(r"[^a-z0-9-]", "", handle)
    # Remove leading and trailing hyphens
    handle = handle.strip("-")
    return handle


def create_product_form(
    name: Annotated[str, Form()],
    # TODO images
    active: Annotated[str, Form()],
    shippable: Annotated[str, Form()],
    preorder: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
) -> schema.ProductCreate:
    handle = get_handle(name)
    return schema.ProductCreate(
        name=name,
        handle=handle,
        description=description,
        active=active == "true",
        shippable=shippable == "true",
        preorder=preorder == "true",
    )


def update_product_form(
    name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    active: Annotated[str | None, Form()] = None,
    shippable: Annotated[str | None, Form()] = None,
    preorder: Annotated[str | None, Form()] = None,
) -> schema.ProductUpdate:
    handle = None
    if name:
        handle = get_handle(name)
    return schema.ProductUpdate(
        name=name,
        handle=handle,
        description=description,
        active=active == "true" if active else None,
        shippable=shippable == "true" if shippable else None,
        preorder=preorder == "true" if shippable else None,
    )
