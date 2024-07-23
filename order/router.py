from sqlmodel import Session
from fastapi import APIRouter, Depends


from order import schema, crud
from lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from lib.session import get_session


router = APIRouter(prefix="/v1/orders")


@router.post("", response_model=schema.OrderList)
def create_order(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    order: schema.OrderCreate = FormDep(schema.OrderCreate),
    db: Session = Depends(get_session),
):
    new_order = crud.create_order(
        shop_id,
        livemode,
        order,
        db,
    )
    return new_order


@router.post("/{order_id}", response_model=schema.Order)
def update_order(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    order_id: str,
    order: schema.OrderUpdate = FormDep(schema.OrderUpdate),
    db: Session = Depends(get_session),
):
    updated_order = crud.update_order(
        shop_id,
        livemode,
        order_id,
        order,
        db,
    )
    return updated_order


@router.get("/{order_id}", response_model=schema.Order)
def retrieve_order(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    order_id: str,
    db: Session = Depends(get_session),
):
    order = crud.retrieve_order(
        shop_id,
        livemode,
        order_id,
        db,
    )
    return order


@router.get("", response_model=schema.OrderList)
def list_orders(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    # TODO skip limit
    orders_list = crud.list_orders(
        shop_id,
        livemode,
        db,
    )
    return orders_list


@router.delete("/{order_id}", response_model=schema.OrderDelete)
def delete_order(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    order_id: str,
    db: Session = Depends(get_session),
):
    deleted_order = crud.delete_order(
        shop_id,
        livemode,
        order_id,
        db,
    )
    return deleted_order
