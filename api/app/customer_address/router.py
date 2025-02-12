from sqlmodel import Session
from fastapi import APIRouter, Depends


from app.customer_address import schema, crud
from app.lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from app.lib.session import get_session

router = APIRouter(prefix="/v1/customer_addresses")


@router.post("", response_model=schema.CustomerAddress)
def create_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    address: schema.CustomerAddressCreate = FormDep(schema.CustomerAddressCreate),
    db: Session = Depends(get_session),
):
    new_address = crud.create_address(
        shop_id,
        livemode,
        address,
        db,
    )
    return new_address


@router.post("/{address_id}", response_model=schema.CustomerAddress)
def update_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    address_id: str,
    address: schema.CustomerAddressUpdate = FormDep(schema.CustomerAddressUpdate),
    db: Session = Depends(get_session),
):
    address = crud.update_address(
        shop_id,
        livemode,
        address_id,
        address,
        db,
    )
    return address


@router.get("/{address_id}", response_model=schema.CustomerAddress)
def retrieve_customer_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    address_id: str,
    db: Session = Depends(get_session),
):
    address = crud.retrieve_address(
        shop_id,
        livemode,
        address_id,
        db,
    )
    return address


@router.get("", response_model=schema.CustomerAddressList)
def list_customer_addresses(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer: str,
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    addresses_list = crud.list_addresses(
        shop_id,
        livemode,
        customer,
        db,
    )
    return addresses_list


@router.delete("/{address_id}", response_model=schema.CustomerAddressDelete)
def delete_customer_address(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    address_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_address(
        shop_id,
        livemode,
        address_id,
        db,
    )
    deleted_address = schema.CustomerAddressDelete(
        id=address_id,
        deleted=deleted_id is not None,
    )
    return deleted_address
