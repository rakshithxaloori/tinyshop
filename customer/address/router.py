from typing import Annotated
from fastapi import APIRouter, Depends


from customer.address import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/customers")


@router.post("/{customer_id}/addresses", response_model=schema.CustomerAddress)
def create_address(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
    address: Annotated[schema.CustomerAddressCreate, Depends(form.create_address_form)],
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
    address: Annotated[schema.CustomerAddressUpdate, Depends(form.update_address_form)],
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
    address = crud.retrieve_address(
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
