from sqlmodel import Session, select

from app.warehouse.model import Warehouse
from app.warehouse import schema
from app.warehouse.utils import pydantify_warehouses
from app.lib.session import update_instance


def create_warehouse(
    shop_id: str,
    livemode: bool,
    warehouse: schema.WarehouseCreate,
    db: Session,
) -> schema.Warehouse | None:
    try:
        warehouse_data = warehouse.model_dump(exclude={"address"})
        wha_data = warehouse.address.model_dump(exclude_none=True)
        new_warehouse = Warehouse(
            shop_id=shop_id,
            livemode=livemode,
            **warehouse_data,
            **wha_data,
        )
        db.add(new_warehouse)

        new_wha = None

        db.commit()
        db.refresh(new_warehouse)
        py_warehouses = pydantify_warehouses([new_warehouse])
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
        wh_ins = results.one()
        update_instance(db, wh_data, wh_ins)

        if warehouse.address:
            wha_data = warehouse.address.model_dump(exclude_none=True)
            update_instance(db, wha_data, wh_ins)
        db.commit()
        db.refresh(wh_ins)
        py_warehouses = pydantify_warehouses([wh_ins])
        return py_warehouses.pop()

    except Exception as e:
        print("EXCEPTION update_warehouse:", e)
        return None


def retrieve_warehouse(
    shop_id: str,
    livemode: bool,
    warehouse_id: str,
    db: Session,
) -> schema.Warehouse | None:
    try:
        results = db.exec(
            select(Warehouse)
            .where(Warehouse.shop_id == shop_id)
            .where(Warehouse.livemode == livemode)
            .where(Warehouse.id == warehouse_id)
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
    results = db.exec(
        select(Warehouse)
        .where(Warehouse.shop_id == shop_id)
        .where(Warehouse.livemode == livemode)
        .offset(skip)
        .limit(limit)
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
    warehouse_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Warehouse)
            .where(Warehouse.shop_id == shop_id)
            .where(Warehouse.livemode == livemode)
            .where(Warehouse.id == warehouse_id)
        )
        warehouse = results.one()
        db.delete(warehouse)
        db.commit()
        return warehouse.id
    except Exception as e:
        print("EXCEPTION delete_warehouse:", e)
        return None
