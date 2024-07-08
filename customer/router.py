from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from customer import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/customers")


@router.post("", response_model=schema.Customer)
def create_customer(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer: Annotated[schema.CustomerCreate, Depends(form.create_customer_form)],
    db: Session = Depends(get_session),
):
    new_customer = crud.create_customer(
        shop_id,
        livemode,
        customer,
        db,
    )
    return new_customer


@router.post("/{customer_id}", response_model=schema.Customer)
def update_customer(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    customer: Annotated[schema.CustomerUpdate, Depends(form.update_customer_form)],
    db: Session = Depends(get_session),
):
    customer = crud.update_customer(
        shop_id,
        livemode,
        customer_id,
        customer,
        db,
    )
    return customer


@router.get("/{customer_id}", response_model=schema.Customer | None)
def retrieve_customer(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    db: Session = Depends(get_session),
):
    customer = crud.retrieve_customer(
        shop_id,
        livemode,
        customer_id,
        db,
    )
    return customer


@router.get("", response_model=schema.CustomerList)
def list_customers(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    customers_list = crud.list_customers(
        shop_id,
        livemode,
        db,
    )
    return customers_list


@router.delete("/{customer_id}", response_model=schema.CustomerDelete)
def delete_customer(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    customer_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_customer(
        shop_id,
        livemode,
        customer_id,
        db,
    )
    return schema.CustomerDelete(
        id=customer_id,
        deleted=deleted_id is not None,
    )


@router.get("/search", response_model=schema.CustomerList)
def search_customers(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    pass
