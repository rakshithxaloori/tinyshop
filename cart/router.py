from typing import Annotated
from fastapi import APIRouter, Depends, Form


from cart import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/carts")


def create_cart_form(
    price: Annotated[str, Form()],
    quantity: Annotated[int, Form()] = 1,
) -> schema.CartCreate:
    return schema.CartCreate(
        cart_item=schema.CartItemCreate(
            price=price,
            quantity=quantity,
        )
    )


def update_cart_form(
    status: Annotated[str, Form()],
) -> schema.CartUpdate:
    return schema.CartUpdate(status=status)


@router.post("", response_model=schema.Cart)
def create_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart: Annotated[schema.CartCreate, Depends(create_cart_form)],
):
    new_cart = crud.create_cart(
        x_shop_id,
        x_livemode,
        cart,
    )
    return new_cart


@router.post("/{cart_id}", response_model=schema.Cart)
def update_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    cart: Annotated[schema.CartUpdate, Depends(update_cart_form)],
):
    updated_cart = crud.update_cart(
        x_shop_id,
        x_livemode,
        cart_id,
        cart,
    )
    return updated_cart


@router.get("/{cart_id}", response_model=schema.Cart)
def retrieve_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
):
    cart = crud.retrieve_cart(
        x_shop_id,
        x_livemode,
        cart_id,
    )
    return cart


@router.get("", response_model=schema.CartList)
def list_carts(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    # TODO skip limit
    carts_list = crud.list_carts(
        x_shop_id,
        x_livemode,
    )
    return carts_list


@router.delete("/{cart_id}", response_model=schema.CartDelete)
def delete_cart(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
):
    deleted_id = crud.delete_cart(
        x_shop_id,
        x_livemode,
        cart_id,
    )
    return schema.CartDelete(
        id=cart_id,
        deleted=deleted_id is not None,
    )
