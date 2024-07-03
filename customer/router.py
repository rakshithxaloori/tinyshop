from typing import Annotated
from fastapi import APIRouter, Depends


from customer import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/customers")


@router.post("", response_model=schema.Customer)
def create_customer(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer: Annotated[schema.CustomerCreate, Depends(form.create_customer_form)],
):
    new_customer = crud.create_customer(
        x_shop_id,
        x_livemode,
        customer,
    )
    return new_customer


@router.post("/{customer_id}", response_model=schema.Customer)
def update_customer(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
    customer: Annotated[schema.CustomerUpdate, Depends(form.update_customer_form)],
):
    updated_customer = crud.update_customer(
        x_shop_id,
        x_livemode,
        customer_id,
        customer,
    )
    return updated_customer


@router.get("/{customer_id}", response_model=schema.Customer | None)
def retrieve_customer(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
):
    customer = crud.retrieve_customer(
        x_shop_id,
        x_livemode,
        customer_id,
    )
    return customer


@router.get("", response_model=schema.CustomerList)
def list_customers(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    # TODO skip, limit
    customers_list = crud.list_customers(
        x_shop_id,
        x_livemode,
    )
    return customers_list


@router.delete("/{customer_id}", response_model=schema.CustomerDelete)
def delete_customer(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
):
    deleted_id = crud.delete_customer(
        x_shop_id,
        x_livemode,
        customer_id,
    )
    return schema.CustomerDelete(
        id=customer_id,
        deleted=deleted_id is not None,
    )


@router.get("/search", response_model=schema.CustomerList)
def search_customers(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    pass
