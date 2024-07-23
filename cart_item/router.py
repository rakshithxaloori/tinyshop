from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query


from cart_item import schema, crud
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session
from lib.dependencies import FormDep

router = APIRouter(prefix="/v1/cart_items")


@router.post("", response_model=schema.CartItem)
def create_cart_item(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart_item: schema.CartItemCreate = FormDep(schema.CartItemCreate),
    db: Session = Depends(get_session),
):
    new_cart_item = crud.create_cart_item(
        shop_id,
        livemode,
        cart_item,
        db,
    )
    return new_cart_item


@router.post("/{cart_item_id}", response_model=schema.CartItem)
def update_cart_item(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart_item_id: str,
    cart_item: schema.CartItemUpdate = FormDep(schema.CartItemUpdate),
    db: Session = Depends(get_session),
):
    cart_item = crud.update_cart_item(
        shop_id,
        livemode,
        cart_item_id,
        cart_item,
        db,
    )
    return cart_item


@router.get("/{cart_item_id}", response_model=schema.CartItem)
def retrieve_cart_item(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart_item_id: str,
    db: Session = Depends(get_session),
):
    cart_item = crud.retrieve_cart_item(
        shop_id,
        livemode,
        cart_item_id,
        db,
    )
    return cart_item


@router.get("", response_model=schema.CartItemList)
def list_cart_items(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart: Annotated[str, Query()],
    db: Session = Depends(get_session),
):
    # TODO skip limit
    cart_items_list = crud.list_cart_items(
        shop_id,
        livemode,
        cart,
        db,
    )
    return cart_items_list


@router.delete("/{cart_item_id}", response_model=schema.CartItemDelete)
def delete_cart_item(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart_item_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_cart_item(
        shop_id,
        livemode,
        cart_item_id,
        db,
    )
    deleted_cart_item = schema.CartItemDelete(
        id=cart_item_id,
        deleted=deleted_id is not None,
    )
    return deleted_cart_item
