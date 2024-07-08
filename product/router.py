from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query


from product import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/products")


@router.post("", response_model=schema.Product)
def create_product(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product: schema.ProductCreate = Depends(form.create_product_form),
    db: Session = Depends(get_session),
):
    new_product = crud.create_product(
        shop_id,
        livemode,
        product,
        db,
    )
    return new_product


@router.post("/{product_id}", response_model=schema.Product)
def update_product(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product_id: str,
    product: schema.ProductUpdate = Depends(form.update_product_form),
    db: Session = Depends(get_session),
):
    product = crud.update_product(
        shop_id,
        livemode,
        product_id,
        product,
        db,
    )
    return product


@router.get("/{product_id}", response_model=schema.Product)
def retrieve_product(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product_id: str,
    expand: Annotated[list[str] | None, Query(alias="expand[]")] = None,
    db: Session = Depends(get_session),
):
    product = crud.retrieve_product(
        shop_id,
        livemode,
        product_id,
        expand,
        db,
    )
    return product


@router.get("", response_model=schema.ProductList)
def list_products(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    expand: Annotated[list[str] | None, Query(alias="expand[]")] = None,
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    print(shop_id, livemode)
    products_list = crud.list_products(
        shop_id,
        livemode,
        expand,
        db,
    )
    return products_list


@router.delete("/{product_id}", response_model=schema.ProductDelete)
def delete_product(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_product(
        shop_id,
        livemode,
        product_id,
        db,
    )
    return schema.ProductDelete(
        id=product_id,
        deleted=deleted_id is not None,
    )
