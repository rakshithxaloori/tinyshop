import re
import unicodedata
from typing import Annotated
from fastapi import APIRouter, Depends, Form


from product import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/products")


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


@router.post("", response_model=schema.Product)
def create_product(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    product: Annotated[schema.Product, Depends(create_product_form)],
):
    new_product = crud.create_product(
        x_shop_id,
        x_livemode,
        product,
    )
    return new_product


@router.post("/{product_id}", response_model=schema.Product)
def update_product(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    product_id: str,
    product: Annotated[schema.Product, Depends(update_product_form)],
):
    updated_product = crud.update_product(
        x_shop_id,
        x_livemode,
        product_id,
        product,
    )
    return updated_product


@router.get("/{product_id}", response_model=schema.Product)
def retrieve_product(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    product_id: str,
):
    product = crud.retrieve_product(
        x_shop_id,
        x_livemode,
        product_id,
    )
    return product


@router.get("", response_model=schema.ProductList)
def list_products(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    # TODO skip, limit
    products_list = crud.list_products(
        x_shop_id,
        x_livemode,
    )
    return products_list


@router.delete("/{product_id}", response_model=schema.ProductDelete)
def delete_product(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    product_id: str,
):
    deleted_id = crud.delete_product(
        x_shop_id,
        x_livemode,
        product_id,
    )
    return schema.ProductDelete(
        id=product_id,
        deleted=deleted_id is not None,
    )
