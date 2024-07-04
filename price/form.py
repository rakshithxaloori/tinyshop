from typing import Annotated
from fastapi import Form


from price import schema


def create_price_form(
    variant: Annotated[str, Form()],
    active: Annotated[str, Form()],
    currency: Annotated[str, Form()],
    price_type: Annotated[str, Form(alias="type")],
    unit_amount: Annotated[int, Form()],
    default: Annotated[str, Form()],
    unit_compare_amount: Annotated[int | None, Form()] = None,
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
) -> schema.PriceCreate:
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
        type=price_type,
        unit_amount=unit_amount,
        unit_compare_amount=unit_compare_amount,
        default=default == "true",
        variant=variant,
        customer_unit_amount=cua,
        recurring=recurring,
    )


def update_price_form(
    active: Annotated[str | None, Form()] = None,
    default: Annotated[str | None, Form()] = None,
    unit_compare_amount: Annotated[int | None, Form()] = None,
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
) -> schema.PriceUpdate:
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
        default=default == "true" if default else None,
        unit_compare_amount=unit_compare_amount,
        customer_unit_amount=cua,
        recurring=recurring,
    )
