from sqlmodel import Session
from fastapi import APIRouter, Depends


from app.cart import schema, crud
from app.lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from app.lib.session import get_session

router = APIRouter(prefix="/v1/carts")


@router.post("", response_model=schema.Cart)
def create_cart(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart: schema.CartCreate = FormDep(schema.CartCreate),
    db: Session = Depends(get_session),
):
    new_cart = crud.create_cart(
        shop_id,
        livemode,
        cart,
        db,
    )
    return new_cart


@router.post("/{cart_id}", response_model=schema.Cart)
def update_cart(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart_id: str,
    cart: schema.CartUpdate = FormDep(schema.CartUpdate),
    db: Session = Depends(get_session),
):
    updated_cart = crud.update_cart(
        shop_id,
        livemode,
        cart_id,
        cart,
        db,
    )
    return updated_cart


@router.get("/{cart_id}", response_model=schema.Cart)
def retrieve_cart(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart_id: str,
    db: Session = Depends(get_session),
):
    cart = crud.retrieve_cart(
        shop_id,
        livemode,
        cart_id,
        db,
    )
    return cart


@router.get("", response_model=schema.CartList)
def list_carts(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    # TODO skip limit
    carts_list = crud.list_carts(
        shop_id,
        livemode,
        db,
    )
    return carts_list


@router.delete("/{cart_id}", response_model=schema.CartDelete)
def delete_cart(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    cart_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_cart(
        shop_id,
        livemode,
        cart_id,
        db,
    )
    return schema.CartDelete(
        id=cart_id,
        deleted=deleted_id is not None,
    )
