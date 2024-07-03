from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from customer.address import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session

router = APIRouter(prefix="/v1/customers")


@router.post("/{customer_id}/addresses", response_model=schema.CustomerAddress)
def create_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    address: Annotated[schema.CustomerAddressCreate, Depends(form.create_address_form)],
    db: Session = Depends(get_session),
):
    new_address = crud.create_address(
        shop_id,
        livemode,
        customer_id,
        address,
        db,
    )
    return new_address


@router.post(
    "/{customer_id}/addresses/{address_id}", response_model=schema.CustomerAddress
)
def update_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    address_id: str,
    address: Annotated[schema.CustomerAddressUpdate, Depends(form.update_address_form)],
    db: Session = Depends(get_session),
):
    updated_address = crud.update_address(
        shop_id,
        livemode,
        customer_id,
        address_id,
        address,
        db,
    )
    return updated_address


@router.get(
    "/{customer_id}/addresses/{address_id}", response_model=schema.CustomerAddress
)
def retrieve_customer_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    address_id: str,
    db: Session = Depends(get_session),
):
    address = crud.retrieve_address(
        shop_id,
        livemode,
        customer_id,
        address_id,
        db,
    )
    return address


@router.get("/{customer_id}/addresses", response_model=schema.CustomerAddressList)
def list_customer_addresses(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    addresses_list = crud.list_addresses(
        shop_id,
        livemode,
        customer_id,
        db,
    )
    return addresses_list


@router.delete(
    "/{customer_id}/addresses/{address_id}", response_model=schema.CustomerAddressDelete
)
def delete_customer_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    address_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_address(
        shop_id,
        livemode,
        customer_id,
        address_id,
        db,
    )
    deleted_address = schema.CustomerAddressDelete(
        id=address_id,
        deleted=deleted_id is not None,
    )
    return deleted_address
