from typing import Annotated
from fastapi import Form

from collection import schema


def create_collection_form(
    name: Annotated[str, Form()],
    image_web: Annotated[str | None, Form()] = None,
    image_mobile: Annotated[str | None, Form()] = None,
    products: Annotated[list[str], Form(alias="products[]")] = [],
) -> schema.CollectionCreate:
    return schema.CollectionCreate(
        name=name,
        image_web=image_web,
        image_mobile=image_mobile,
        products=products,
    )


def update_collection_form(
    name: Annotated[str | None, Form()] = None,
    image_web: Annotated[str | None, Form()] = None,
    image_mobile: Annotated[str | None, Form()] = None,
    products_add: Annotated[list[str], Form(alias="products[add][]")] = [],
    products_remove: Annotated[list[str], Form(alias="products[remove][]")] = [],
) -> schema.CollectionUpdate:
    return schema.CollectionUpdate(
        name=name,
        image_web=image_web,
        image_mobile=image_mobile,
        products=schema.ProductsUpdate(
            add=products_add,
            remove=products_remove,
        ),
    )
