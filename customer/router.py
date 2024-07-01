from typing import Annotated
from fastapi import APIRouter, Depends, Form
from pydantic import BaseModel


from customer import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep, is_livemode

router = APIRouter(prefix="/v1/customers")


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


@router.post("", response_model=schema.Customer)
async def create_customer(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer: Annotated[schema.CustomerCreate, Depends(create_customer_form)],
):
    new_customer = crud.create_customer(
        x_shop_id,
        is_livemode(x_livemode),
        customer,
    )
    return new_customer


@router.post("/{customer_id}", response_model=schema.Customer)
def update_customer(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
    customer: Annotated[schema.CustomerUpdate, Depends(update_customer_form)],
):
    updated_customer = crud.update_customer(
        x_shop_id,
        is_livemode(x_livemode),
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
        is_livemode(x_livemode),
        customer_id,
    )
    return customer


@router.get("", response_model=schema.CustomerList)
def list_customers(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    customers = crud.list_customers(
        x_shop_id,
        is_livemode(x_livemode),
    )
    return schema.CustomerList(
        has_more=False,
        data=customers,
    )


@router.delete("/{customer_id}", response_model=schema.CustomerDelete)
def delete_customer(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    customer_id: str,
):
    deleted_id = crud.delete_customer(
        x_shop_id,
        is_livemode(x_livemode),
        customer_id,
    )
    deleted_customer = schema.CustomerDelete(
        id=customer_id, deleted=deleted_id is not None
    )
    return deleted_customer


@router.get("/search", response_model=schema.CustomerList)
def search_customers(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    pass
