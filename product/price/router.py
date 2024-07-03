from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from product.price import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session

router = APIRouter(prefix="/v1/prices")


@router.post("", response_model=schema.Price)
def create_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price: Annotated[schema.PriceCreate, Depends(form.create_price_form)],
    db: Annotated[Session, Depends(get_session)],
):
    new_price = crud.create_price(
        x_shop_id,
        x_livemode,
        price,
        db,
    )
    return new_price


@router.post("/{price_id}", response_model=schema.Price)
def update_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price_id: str,
    price: Annotated[schema.PriceUpdate, Depends(form.update_price_form)],
    db: Annotated[Session, Depends(get_session)],
):
    updated_price = crud.update_price(
        x_shop_id,
        x_livemode,
        price_id,
        price,
        db,
    )
    return updated_price


@router.get("/{price_id}", response_model=schema.Price)
def retrieve_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price_id: str,
    db: Annotated[Session, Depends(get_session)],
):
    price = crud.retrieve_price(
        x_shop_id,
        x_livemode,
        price_id,
        db,
    )
    return price


@router.get("", response_model=schema.PriceList)
def list_prices(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    db: Annotated[Session, Depends(get_session)],
):
    price_list = crud.list_prices(
        x_shop_id,
        x_livemode,
        db,
    )
    return price_list


@router.delete("/{price_id}", response_model=schema.PriceDelete)
def delete_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price_id: str,
    db: Annotated[Session, Depends(get_session)],
):
    deleted_id = crud.delete_customer(
        x_shop_id,
        x_livemode,
        price_id,
        db,
    )
    deleted_price = schema.PriceDelete(id=price_id, deleted=deleted_id is not None)
    return deleted_price
