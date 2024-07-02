from typing import Annotated
from fastapi import APIRouter, Depends, Form


from cart.cart_item import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/carts")


def create_cart_item_form(
    cart: Annotated[str, Form()],
    price: Annotated[str, Form()],
    quantity: Annotated[int, Form()] = 1,
) -> schema.CartItemCreate:
    return schema.CartItemCreate(
        cart=cart,
        price=price,
        quantity=quantity,
    )


def update_cart_item_form(
    quantity: Annotated[int, Form()],
) -> schema.CartItemUpdate:
    return schema.CartItemUpdate(quantity=quantity)


@router.post("/{cart_id}/cart_items", response_model=schema.CartItem)
def create_cart_item(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    cart_item: Annotated[schema.CartItemCreate, Depends(create_cart_item_form)],
):
    new_cart_item = crud.create_cart_item(
        x_shop_id,
        x_livemode,
        cart_id,
        cart_item,
    )
    return new_cart_item


@router.post(
    "/{cart_id}/cart_items/{cart_item_id}", response_model=schema.CartItemUpdate
)
def update_cart_item(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    cart_item_id: str,
    cart_item: Annotated[schema.CartItemUpdate, Depends(update_cart_item_form)],
):
    updated_cart_item = crud.update_cart_item(
        x_shop_id,
        x_livemode,
        cart_id,
        cart_item_id,
        cart_item,
    )
    return updated_cart_item


@router.get("/{cart_id}/cart_items/{cart_item_id}", response_model=schema.CartItem)
def retrieve_cart_item(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    cart_item_id: str,
):
    cart_item = crud.retrieve_cart_item(
        x_shop_id,
        x_livemode,
        cart_id,
        cart_item_id,
    )
    return cart_item


@router.get("/{cart_id}/cart_items", response_model=schema.CartItemList)
def list_cart_items(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
):
    # TODO skip limit
    cart_items_list = crud.list_cart_items(
        x_shop_id,
        x_livemode,
        cart_id,
    )
    return cart_items_list


@router.delete(
    "/{cart_id}/cart_items/{cart_item_id}", response_model=schema.CartItemDelete
)
def delete_cart_item(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    cart_id: str,
    cart_item_id: str,
):
    deleted_id = crud.delete_cart_item(
        x_shop_id,
        x_livemode,
        cart_id,
        cart_item_id,
    )
    deleted_cart_item = schema.CartItemDelete(
        id=cart_item_id,
        deleted=deleted_id is not None,
    )
    return deleted_cart_item
