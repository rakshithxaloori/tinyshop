from typing import Annotated
from fastapi import APIRouter, Depends, Form


from product.option import schema, crud
from lib.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/options")


def create_option_form(
    name: Annotated[str, Form()],
    values: Annotated[list[str], Form()],
    product: Annotated[str, Form()],
):
    return schema.OptionCreate(
        name=name,
        values=values,
        product=product,
    )


def update_option_form(
    name: Annotated[str | None, Form()],
    values: Annotated[list[str] | None, Form()],
):
    return schema.OptionUpdate(
        name=name,
        values=values,
    )


@router.post("", response_model=schema.Option)
def create_option(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    option: Annotated[schema.OptionCreate, Depends(create_option_form)],
):
    new_option = crud.create_option(
        x_shop_id,
        x_livemode,
        option,
    )
    return new_option


@router.post("/{option_id}", response_model=schema.Option)
def update_option(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    option_id: str,
    option: Annotated[schema.OptionUpdate, Depends(update_option_form)],
):
    updated_option = crud.update_option(
        x_shop_id,
        x_livemode,
        option_id,
        option,
    )
    return updated_option


@router.get("/{option_id}", response_model=schema.Option)
def retrieve_option(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    option_id: str,
):
    option = crud.retrieve_option(
        x_shop_id,
        x_livemode,
        option_id,
    )
    return option


@router.get("", response_model=schema.OptionList)
def list_options(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    # TODO skip, limit
    options_list = crud.list_options(
        x_shop_id,
        x_livemode,
    )
    return options_list


@router.delete("/{option_id}", response_model=schema.OptionDelete)
def delete_option(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    option_id: str,
):
    deleted_id = crud.delete_option(
        x_shop_id,
        x_livemode,
        option_id,
    )
    deleted_option = schema.OptionDelete(
        id=option_id,
        deleted=deleted_id is not None,
    )
    return deleted_option
