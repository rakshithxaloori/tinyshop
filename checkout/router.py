from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from checkout import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/checkouts")


@router.post("", response_model=schema.Checkout)
def create_checkout(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    checkout: Annotated[schema.CheckoutCreate, Depends(form.create_checkout_form)],
    db: Session = Depends(get_session),
):
    new_checkout = crud.create_checkout(
        shop_id,
        livemode,
        checkout,
        db,
    )
    return new_checkout


@router.post("/{checkout_id}", response_model=schema.Checkout)
def update_checkout(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    checkout_id: str,
    checkout: Annotated[schema.CheckoutUpdate, Depends(form.update_checkout_form)],
    db: Session = Depends(get_session),
):
    updated_checkout = crud.update_checkout(
        shop_id,
        livemode,
        checkout_id,
        checkout,
        db,
    )
    return updated_checkout


@router.get("/{checkout_id}", response_model=schema.Checkout)
def retrieve_checkout(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    checkout_id: str,
    db: Session = Depends(get_session),
):
    checkout = crud.retrieve_checkout(
        shop_id,
        livemode,
        checkout_id,
        db,
    )
    return checkout


@router.get("", response_model=schema.CheckoutList)
def list_checkouts(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    checkouts_list = crud.list_checkouts(
        shop_id,
        livemode,
        db,
    )
    return checkouts_list


@router.delete("/{checkout_id}", response_model=schema.CheckoutDelete)
def delete_checkout(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    checkout_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_checkout(
        shop_id,
        livemode,
        checkout_id,
        db,
    )
    deleted_option = schema.CheckoutDelete(
        id=checkout_id,
        deleted=deleted_id is not None,
    )
    return deleted_option
