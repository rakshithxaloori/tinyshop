from typing import Annotated
from fastapi import Form


from customer_address import schema


def create_address_form(
    customer: Annotated[str, Form()],
    name: Annotated[str, Form()],
    line1: Annotated[str, Form()],
    city: Annotated[str, Form()],
    state: Annotated[str, Form()],
    country: Annotated[str, Form()],
    postal_code: Annotated[str, Form()],
    line2: Annotated[str | None, Form()] = None,
) -> schema.CustomerAddressCreate:
    return schema.CustomerAddressCreate(
        customer=customer,
        name=name,
        line1=line1,
        line2=line2,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code,
    )


def update_address_form(
    name: Annotated[str | None, Form(alias="name")] = None,
    line1: Annotated[str | None, Form(alias="line1")] = None,
    line2: Annotated[str | None, Form(alias="line2")] = None,
    city: Annotated[str | None, Form(alias="city")] = None,
    state: Annotated[str | None, Form(alias="state")] = None,
    country: Annotated[str | None, Form(alias="country")] = None,
    postal_code: Annotated[str | None, Form(alias="postal_code")] = None,
) -> schema.CustomerAddressUpdate:
    return schema.CustomerAddressUpdate(
        name=name,
        line1=line1,
        line2=line2,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code,
    )
