from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from cart import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session

router = APIRouter(prefix="/v1/carts")


@router.post("", response_model=schema.Cart)
def create_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart: Annotated[schema.CartCreate, Depends(form.create_cart_form)],
    db: Annotated[Session, Depends(get_session)],
):
    new_cart = crud.create_cart(
        x_shop_id,
        x_livemode,
        cart,
        db,
    )
    return new_cart


@router.post("/{cart_id}", response_model=schema.Cart)
def update_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    cart: Annotated[schema.CartUpdate, Depends(form.update_cart_form)],
    db: Annotated[Session, Depends(get_session)],
):
    updated_cart = crud.update_cart(
        x_shop_id,
        x_livemode,
        cart_id,
        cart,
        db,
    )
    return updated_cart


@router.get("/{cart_id}", response_model=schema.Cart)
def retrieve_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    db: Annotated[Session, Depends(get_session)],
):
    cart = crud.retrieve_cart(
        x_shop_id,
        x_livemode,
        cart_id,
        db,
    )
    return cart


@router.get("", response_model=schema.CartList)
def list_carts(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    db: Annotated[Session, Depends(get_session)],
):
    # TODO skip limit
    carts_list = crud.list_carts(
        x_shop_id,
        x_livemode,
        db,
    )
    return carts_list


@router.delete("/{cart_id}", response_model=schema.CartDelete)
def delete_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    db: Annotated[Session, Depends(get_session)],
):
    deleted_id = crud.delete_cart(
        x_shop_id,
        x_livemode,
        cart_id,
        db,
    )
    return schema.CartDelete(
        id=cart_id,
        deleted=deleted_id is not None,
    )
