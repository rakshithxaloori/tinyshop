from typing import Annotated
from fastapi import Form


from warehouse import schema


def create_warehouse_form(
    name: Annotated[str, Form()],
    active: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    address_line1: Annotated[str, Form(alias="address[line1]")],
    address_line2: Annotated[str, Form(alias="address[line2]")],
    address_city: Annotated[str, Form(alias="address[city]")],
    address_state: Annotated[str, Form(alias="address[state]")],
    address_country: Annotated[str, Form(alias="address[country]")],
    address_postal_code: Annotated[str, Form(alias="address[postal_code]")],
) -> schema.WarehouseCreate:
    return schema.WarehouseCreate(
        name=name,
        active=active == "true",
        phone=phone,
        address=schema.WarehouseAddress(
            line1=address_line1,
            line2=address_line2,
            city=address_city,
            state=address_state,
            country=address_country,
            postal_code=address_postal_code,
        ),
    )


def update_warehouse_form(
    name: Annotated[str | None, Form()] = None,
    active: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    address_line1: Annotated[str | None, Form(alias="address[line1]")] = None,
    address_line2: Annotated[str | None, Form(alias="address[line2]")] = None,
    address_city: Annotated[str | None, Form(alias="address[city]")] = None,
    address_state: Annotated[str | None, Form(alias="address[state]")] = None,
    address_country: Annotated[str | None, Form(alias="address[country]")] = None,
    address_postal_code: Annotated[
        str | None, Form(alias="address[postal_code]")
    ] = None,
) -> schema.WarehouseUpdate:
    return schema.WarehouseUpdate(
        name=name,
        active=active == "true" if active else None,
        phone=phone,
        address=schema.WarehouseAddress(
            line1=address_line1,
            line2=address_line2,
            city=address_city,
            state=address_state,
            country=address_country,
            postal_code=address_postal_code,
        ),
    )
