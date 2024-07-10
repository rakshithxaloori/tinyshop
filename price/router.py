from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query


from price import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session

router = APIRouter(prefix="/v1/prices")


@router.post("", response_model=schema.Price)
def create_price(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    price: Annotated[schema.PriceCreate, Depends(form.create_price_form)],
    db: Session = Depends(get_session),
):
    new_price = crud.create_price(
        shop_id,
        livemode,
        price,
        db,
    )
    return new_price


@router.post("/{price_id}", response_model=schema.Price)
def update_price(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    price_id: str,
    price: Annotated[schema.PriceUpdate, Depends(form.update_price_form)],
    db: Session = Depends(get_session),
):
    price = crud.update_price(
        shop_id,
        livemode,
        price_id,
        price,
        db,
    )
    return price


@router.get("/{price_id}", response_model=schema.Price)
def retrieve_price(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    price_id: str,
    db: Session = Depends(get_session),
):
    price = crud.retrieve_price(
        shop_id,
        livemode,
        price_id,
        db,
    )
    return price


@router.get("", response_model=schema.PriceList)
def list_prices(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    variant: Annotated[str, Query()],
    db: Session = Depends(get_session),
):
    price_list = crud.list_prices(
        shop_id,
        livemode,
        variant,
        db,
    )
    return price_list


@router.delete("/{price_id}", response_model=schema.PriceDelete)
def delete_price(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    price_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_price(
        shop_id,
        livemode,
        price_id,
        db,
    )
    deleted_price = schema.PriceDelete(
        id=price_id,
        deleted=deleted_id is not None,
    )
    return deleted_price
