from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from discount import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/discounts")


@router.post("", response_model=schema.Discount)
def create_discount(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    discount: Annotated[schema.DiscountCreate, Depends(form.create_discount_form)],
    db: Session = Depends(get_session),
):
    new_discount = crud.create_discount(
        shop_id,
        livemode,
        discount,
        db,
    )
    return new_discount


@router.post("/{discount_id}", response_model=schema.Discount)
def update_discount(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    discount_id: str,
    discount: Annotated[schema.DiscountUpdate, Depends(form.update_discount_form)],
    db: Session = Depends(get_session),
):
    discount = crud.update_discount(
        shop_id,
        livemode,
        discount_id,
        discount,
        db,
    )
    return discount


@router.get("/{discount_id}", response_model=schema.Discount)
def retrieve_discount(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    discount_id: str,
    db: Session = Depends(get_session),
):
    discount = crud.retrieve_discount(
        shop_id,
        livemode,
        discount_id,
        db,
    )
    return discount


@router.get("", response_model=schema.DiscountList)
def list_discounts(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    discounts_list = crud.list_discounts(
        shop_id,
        livemode,
        db,
    )
    return discounts_list


@router.delete("/{discount_id}", response_model=schema.DiscountDelete)
def delete_discount(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    discount_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_discount(
        shop_id,
        livemode,
        discount_id,
        db,
    )
    deleted_discount = schema.DiscountDelete(
        id=discount_id,
        deleted=deleted_id is not None,
    )
    return deleted_discount
