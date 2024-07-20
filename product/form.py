from typing import Annotated
from fastapi import Form


from product import schema
from lib.form.sanitizers import bool_sanitizer, urls_sanitizer
from lib.form.handle import get_handle


def create_product_form(
    name: Annotated[str, Form()],
    active: Annotated[str, Form()],
    shippable: Annotated[str, Form()],
    preorder: Annotated[str, Form()],
    images: Annotated[set[str], Form(alias="images[]")] = None,
    description: Annotated[str | None, Form()] = None,
) -> schema.ProductCreate:
    # Sanitize the all fields of the form
    name: str = name.strip()
    active: bool = bool_sanitizer(active, "active")
    shippable: bool = bool_sanitizer(shippable, "shippable")
    preorder: bool = bool_sanitizer(preorder, "preorder")
    images: set[str] = urls_sanitizer(images, "images", count_max=8)

    handle = get_handle(name)
    return schema.ProductCreate(
        name=name,
        images=images,
        handle=handle,
        description=description,
        active=active,
        shippable=shippable,
        preorder=preorder,
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
        preorder=preorder == "true" if preorder else None,
    )
