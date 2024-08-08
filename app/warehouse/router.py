from sqlmodel import Session
from fastapi import APIRouter, Depends


from app.warehouse import schema, crud
from app.lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from app.lib.session import get_session


router = APIRouter(prefix="/v1/warehouses")


@router.post("", response_model=schema.Warehouse)
def create_warehouse(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    warehouse: schema.WarehouseCreate = FormDep(schema.WarehouseCreate),
    db: Session = Depends(get_session),
):
    new_warehouse = crud.create_warehouse(
        shop_id,
        livemode,
        warehouse,
        db,
    )
    return new_warehouse


@router.post("/{warehouse_id}", response_model=schema.Warehouse)
def update_warehouse(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    warehouse_id: str,
    warehouse: schema.WarehouseUpdate = FormDep(schema.WarehouseUpdate),
    db: Session = Depends(get_session),
):
    warehouse = crud.update_warehouse(
        shop_id,
        livemode,
        warehouse_id,
        warehouse,
        db,
    )
    return warehouse


@router.get("/{warehouse_id}", response_model=schema.Warehouse)
def retrieve_warehouse(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    warehouse_id: str,
    db: Session = Depends(get_session),
):
    warehouse = crud.retrieve_warehouse(
        shop_id,
        livemode,
        warehouse_id,
        db,
    )
    return warehouse


@router.get("", response_model=schema.WarehouseList)
def list_warehouses(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    warehouses_list = crud.list_warehouses(
        shop_id,
        livemode,
        db,
    )
    return warehouses_list


@router.delete("/{warehouse_id}", response_model=schema.WarehouseDelete)
def delete_warehouse(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    warehouse_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_warehouse(
        shop_id,
        livemode,
        warehouse_id,
        db,
    )
    return schema.WarehouseDelete(
        id=warehouse_id,
        deleted=deleted_id is not None,
    )
