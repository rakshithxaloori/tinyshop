from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query


from option import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/options")


@router.post("", response_model=schema.Option)
def create_option(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    option: Annotated[schema.OptionCreate, Depends(form.create_option_form)],
    db: Session = Depends(get_session),
):
    new_option = crud.create_option(
        shop_id,
        livemode,
        option,
        db,
    )
    return new_option


@router.post("/{option_id}", response_model=schema.Option)
def update_option(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    option_id: str,
    option: Annotated[schema.OptionUpdate, Depends(form.update_option_form)],
    db: Session = Depends(get_session),
):
    updated_option = crud.update_option(
        shop_id,
        livemode,
        option_id,
        option,
        db,
    )
    return updated_option


@router.get("/{option_id}", response_model=schema.Option)
def retrieve_option(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    option_id: str,
    db: Session = Depends(get_session),
):
    option = crud.retrieve_option(
        shop_id,
        livemode,
        option_id,
        db,
    )
    return option


@router.get("", response_model=schema.OptionList)
def list_options(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product: Annotated[str, Query()],
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    options_list = crud.list_options(
        shop_id,
        livemode,
        product,
        db,
    )
    return options_list


@router.delete("/{option_id}", response_model=schema.OptionDelete)
def delete_option(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    option_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_option(
        shop_id,
        livemode,
        option_id,
        db,
    )
    deleted_option = schema.OptionDelete(
        id=option_id,
        deleted=deleted_id is not None,
    )
    return deleted_option
