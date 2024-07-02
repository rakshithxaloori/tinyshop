from typing import Annotated
from fastapi import APIRouter, Depends, Form


from customer.address import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/customers")


def create_address_form(
    name: Annotated[str, Form(alias="name")],
    line1: Annotated[str, Form(alias="line1")],
    city: Annotated[str, Form(alias="city")],
    state: Annotated[str, Form(alias="state")],
    country: Annotated[str, Form(alias="country")],
    postal_code: Annotated[str, Form(alias="postal_code")],
    line2: Annotated[str | None, Form(alias="line2")] = None,
) -> schema.CustomerAddressCreate:
    return schema.CustomerAddressCreate(
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


@router.post("/{customer_id}/addresses", response_model=schema.CustomerAddress)
def create_address(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
    address: Annotated[schema.CustomerAddressCreate, Depends(create_address_form)],
):
    new_address = crud.create_address(
        x_shop_id,
        x_livemode,
        customer_id,
        address,
    )
    return new_address


@router.post(
    "/{customer_id}/addresses/{address_id}", response_model=schema.CustomerAddress
)
def update_address(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
    address_id: str,
    address: Annotated[schema.CustomerAddressUpdate, Depends(update_address_form)],
):
    updated_address = crud.update_address(
        x_shop_id,
        x_livemode,
        customer_id,
        address_id,
        address,
    )
    return updated_address


@router.get(
    "/{customer_id}/addresses/{address_id}", response_model=schema.CustomerAddress
)
def retrieve_customer_address(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
    address_id: str,
):
    address = crud.retrieve_customer(
        x_shop_id,
        x_livemode,
        customer_id,
        address_id,
    )
    return address


@router.get("/{customer_id}/addresses", response_model=schema.CustomerAddressList)
def list_customer_addresses(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
):
    # TODO skip, limit
    addresses_list = crud.list_addresses(
        x_shop_id,
        x_livemode,
        customer_id,
    )
    return addresses_list


@router.delete(
    "/{customer_id}/addresses/{address_id}", response_model=schema.CustomerAddressDelete
)
def delete_customer_address(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
    address_id: str,
):
    deleted_id = crud.delete_address(
        x_shop_id,
        x_livemode,
        customer_id,
        address_id,
    )
    deleted_address = schema.CustomerAddressDelete(
        id=address_id,
        deleted=deleted_id is not None,
    )
    return deleted_address
