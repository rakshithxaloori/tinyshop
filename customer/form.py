from typing import Annotated
from fastapi import Form


from customer import schema


def create_customer_form(
    name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str | None, Form()] = None,
    address_name: Annotated[str | None, Form(alias="address[name]")] = None,
    address_line1: Annotated[str | None, Form(alias="address[line1]")] = None,
    address_line2: Annotated[str | None, Form(alias="address[line2]")] = None,
    address_city: Annotated[str | None, Form(alias="address[city]")] = None,
    address_state: Annotated[str | None, Form(alias="address[state]")] = None,
    address_country: Annotated[str | None, Form(alias="address[country]")] = None,
    address_postal_code: Annotated[
        str | None, Form(alias="address[postal_code]")
    ] = None,
) -> schema.CustomerCreate:
    new_address: schema.CustomerAddressCreate | None = None
    try:
        new_address = schema.CustomerAddressCreate(
            name=address_name,
            line1=address_line1,
            line2=address_line2,
            city=address_city,
            state=address_state,
            country=address_country,
            postal_code=address_postal_code,
        )
    except Exception:
        new_address = None
    return schema.CustomerCreate(
        name=name, phone=phone, email=email, address=new_address
    )


def update_customer_form(
    name: Annotated[str | None, Form()] = None,
    phone: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
) -> schema.CustomerUpdate:
    return schema.CustomerUpdate(name=name, phone=phone, email=email)
