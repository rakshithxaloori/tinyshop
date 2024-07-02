from typing import Annotated
from fastapi import APIRouter, Depends, Form


from product.price import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep

router = APIRouter(prefix="/v1/prices")


def create_price_form(
    active: Annotated[str, Form()],
    currency: Annotated[str, Form()],
    type: Annotated[str, Form()],
    unit_amount: Annotated[int, Form()],
    default: Annotated[str, Form()],
    variant: Annotated[str, Form()],
    customer_unit_amount_maximum: Annotated[
        str | None, Form(alias="customer_unit_amount[maximum]")
    ] = None,
    customer_unit_amount_minimum: Annotated[
        str | None, Form(alias="customer_unit_amount[minimum]")
    ] = None,
    customer_unit_amount_preset: Annotated[
        str | None, Form(alias="customer_unit_amount[preset]")
    ] = None,
    recurring_interval: Annotated[str | None, Form(alias="recurring[interval]")] = None,
    recurring_interval_count: Annotated[
        str | None, Form(alias="recurring[interval_count]")
    ] = None,
):
    # TODO validation
    cua = None
    if (
        customer_unit_amount_maximum
        or customer_unit_amount_minimum
        or customer_unit_amount_preset
    ):
        cua = schema.CustomerUnitAmount(
            maximum=customer_unit_amount_maximum,
            minimum=customer_unit_amount_minimum,
            preset=customer_unit_amount_preset,
        )
    recurring = None
    if recurring_interval and recurring_interval_count:
        recurring = schema.Recurring(
            interval=recurring_interval,
            interval_count=recurring_interval_count,
        )
    return schema.PriceCreate(
        active=active == "true",
        currency=currency,
        type=type,
        unit_amount=unit_amount,
        default=default == "true",
        variant=variant,
        customer_unit_amount=cua,
        recurring=recurring,
    )


def update_price_form(
    active: Annotated[str | None, Form()] = None,
    currency: Annotated[str | None, Form()] = None,
    type: Annotated[str | None, Form()] = None,
    unit_amount: Annotated[int | None, Form()] = None,
    default: Annotated[str | None, Form()] = None,
    variant: Annotated[str | None, Form()] = None,
    customer_unit_amount_maximum: Annotated[
        str | None, Form(alias="customer_unit_amount[maximum]")
    ] = None,
    customer_unit_amount_minimum: Annotated[
        str | None, Form(alias="customer_unit_amount[minimum]")
    ] = None,
    customer_unit_amount_preset: Annotated[
        str | None, Form(alias="customer_unit_amount[preset]")
    ] = None,
    recurring_interval: Annotated[str | None, Form(alias="recurring[interval]")] = None,
    recurring_interval_count: Annotated[
        str | None, Form(alias="recurring[interval_count]")
    ] = None,
):
    # TODO validation
    cua = None
    if (
        customer_unit_amount_maximum
        or customer_unit_amount_minimum
        or customer_unit_amount_preset
    ):
        cua = schema.CustomerUnitAmount(
            maximum=customer_unit_amount_maximum,
            minimum=customer_unit_amount_minimum,
            preset=customer_unit_amount_preset,
        )
    recurring = None
    if recurring_interval and recurring_interval_count:
        recurring = schema.Recurring(
            interval=recurring_interval,
            interval_count=recurring_interval_count,
        )
    return schema.PriceUpdate(
        active=active == "true" if active else None,
        currency=currency,
        type=type,
        unit_amount=unit_amount,
        default=default == "true" if default else None,
        variant=variant,
        customer_unit_amount=cua,
        recurring=recurring,
    )


@router.post("", response_model=schema.Price)
def create_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price: Annotated[schema.PriceCreate, Depends(create_price_form)],
):
    new_price = crud.create_price(
        x_shop_id,
        x_livemode,
        price,
    )
    return new_price


@router.post("/{price_id}", response_model=schema.Price)
def update_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price_id: str,
    price: Annotated[schema.PriceCreate, Depends(update_price_form)],
):
    updated_price = crud.update_price(
        x_shop_id,
        x_livemode,
        price_id,
        price,
    )
    return updated_price


@router.get("/{price_id}", response_model=schema.Price)
def retrieve_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price_id: str,
):
    price = crud.retrieve_price(
        x_shop_id,
        x_livemode,
        price_id,
    )
    return price


@router.get("", response_model=schema.PriceList)
def list_prices(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    price_list = crud.list_prices(
        x_shop_id,
        x_livemode,
    )
    return price_list


@router.delete("/{price_id}", response_model=schema.PriceDelete)
def delete_price(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    price_id: str,
):
    deleted_id = crud.delete_customer(
        x_shop_id,
        x_livemode,
        price_id,
    )
    deleted_price = schema.PriceDelete(id=price_id, deleted=deleted_id is not None)
    return deleted_price
