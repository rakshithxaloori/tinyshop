from sqlmodel import Session, select

from warehouse.model import Warehouse, WarehouseAddress
from warehouse import schema
from warehouse.utils import pydantify_warehouses
from lib.session import update_instance


def create_warehouse(
    shop_id: str,
    livemode: bool,
    warehouse: schema.WarehouseCreate,
    db: Session,
) -> schema.Warehouse | None:
    try:
        warehouse_data = warehouse.model_dump(exclude={"address"})
        new_warehouse = Warehouse(
            shop_id=shop_id,
            livemode=livemode,
            **warehouse_data,
        )
        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)

        new_wha = None
        if warehouse.address:
            wha_data = warehouse.address.model_dump(exclude_none=True)
            new_wha = WarehouseAddress(
                shop_id=shop_id,
                livemode=livemode,
                warehouse_id=new_warehouse.id,
                **wha_data,
            )
            db.add(new_wha)
            db.commit()
            db.refresh(new_warehouse)
            db.refresh(new_wha)
        py_warehouses = pydantify_warehouses([(new_warehouse, new_wha)])
        return py_warehouses.pop()

    except Exception as e:
        print("EXCEPTION create_warehouse:", e)
        return None


def update_warehouse(
    shop_id: str,
    livemode: bool,
    warehouse_id: str,
    warehouse: schema.WarehouseUpdate,
    db: Session,
) -> schema.Warehouse | None:
    try:
        wh_data = warehouse.model_dump(exclude_none=True, exclude={"address"})

        statement = (
            select(Warehouse)
            .where(Warehouse.shop_id == shop_id)
            .where(Warehouse.livemode == livemode)
            .where(Warehouse.id == warehouse_id)
        )
        results = db.exec(statement)
        updated_wh = results.one()
        update_instance(db, wh_data, updated_wh)

        wha = None
        if warehouse.address:
            wha_data = warehouse.address.model_dump(exclude_none=True)
            print("WHA DATA", wha_data)
            statement = select(WarehouseAddress).where(
                WarehouseAddress.warehouse_id == warehouse_id
            )
            results = db.exec(statement)
            wha = results.one()
            update_instance(db, wha_data, wha)
            db.refresh(updated_wh)
        py_warehouses = pydantify_warehouses([(updated_wh, wha)])
        return py_warehouses.pop()

    except Exception as e:
        print("EXCEPTION update_warehouse:", e)
        return None


def retrieve_warehouse(
    shop_id: str,
    livemode: bool,
    id: str,
    db: Session,
) -> schema.Warehouse | None:
    try:
        results = db.exec(
            select(Warehouse, WarehouseAddress)
            .where(Warehouse.shop_id == shop_id)
            .where(Warehouse.livemode == livemode)
            .where(Warehouse.id == id)
            .where(
                Warehouse.id == WarehouseAddress.warehouse_id
            )  # TODO this is optional, TODO for customer address too
        )
        wh = results.one()
        py_warehouses = pydantify_warehouses([wh])
        return py_warehouses.pop()
    except Exception as e:
        print("EXCEPTION retrieve_warehouse", e)
        return None


def list_warehouses(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.WarehouseList:
    subquery = select(Warehouse.id).offset(skip).limit(limit).subquery()

    results = db.exec(
        select(Warehouse, WarehouseAddress)
        .where(Warehouse.shop_id == shop_id)
        .where(Warehouse.livemode == livemode)
        .where(Warehouse.id.in_(subquery))
        .where(Warehouse.id == WarehouseAddress.warehouse_id)
    )
    all_rows = list(results.all())
    warehouses = pydantify_warehouses(all_rows)
    return schema.WarehouseList(
        url="/v1/warehouses",
        has_more=False,  # TODO
        data=warehouses,
    )


def delete_warehouse(
    shop_id: str,
    livemode: bool,
    id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Warehouse)
            .where(Warehouse.shop_id == shop_id)
            .where(Warehouse.livemode == livemode)
            .where(Warehouse.id == id)
        )
        warehouse = results.one()
        db.delete(warehouse)
        db.commit()
        return warehouse.id
    except Exception as e:
        print("EXCEPTION delete_warehouse:", e)
        return None
