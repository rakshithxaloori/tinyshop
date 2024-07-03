from sqlmodel import Session, select

from warehouse.model import Warehouse
from product.variant.model import Variant
from warehouse.inventory.model import Inventory
from warehouse.inventory import schema
from warehouse.inventory.utils import pydantify_inventories
from lib.session import update_refresh


def create_inventory(
    shop_id: str,
    livemode: bool,
    inventory: schema.InventoryCreate,
    db: Session,
) -> schema.Inventory | None:
    try:
        variant_res = db.exec(
            select(Variant)
            .where(Variant.shop_id == shop_id)
            .where(Variant.livemode == livemode)
            .where(Variant.id == inventory.variant)
        )
        variant = variant_res.one()

        warehouse_res = db.exec(
            select(Warehouse)
            .where(Warehouse.shop_id == shop_id)
            .where(Warehouse.livemode == livemode)
            .where(Warehouse.id == inventory.warehouse)
        )
        warehouse = warehouse_res.one()

        inventory_data = inventory.model_dump(exclude={"warehouse", "variant"})
        new_inventory = Inventory(
            shop_id=shop_id,
            livemode=livemode,
            variant_id=variant.id,
            warehouse_id=warehouse.id,
            **inventory_data,
        )
        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)
        py_inventories = pydantify_inventories([new_inventory])
        return py_inventories.pop()
    except Exception as e:
        print("EXCEPTION create_inventory:", e)
        return None


def update_inventory(
    shop_id: str,
    livemode: bool,
    id: str,
    inventory: schema.InventoryUpdate,
    db: Session,
) -> schema.Inventory | None:
    try:
        in_data = inventory.model_dump(exclude_none=True)
        results = db.exec(
            select(Inventory)
            .where(Inventory.shop_id == shop_id)
            .where(Inventory.livemode == livemode)
            .where(Inventory.id == id)
        )
        inventory = results.one()
        update_refresh(db, in_data, inventory)
        py_inventories = pydantify_inventories([inventory])
        return py_inventories.pop()

    except Exception as e:
        print("EXCEPTION update_inventory:", e)
        return None


def delete_inventory(
    shop_id: str,
    livemode: bool,
    id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Inventory)
            .where(Inventory.shop_id == shop_id)
            .where(Inventory.livemode == livemode)
            .where(Inventory.id == id)
        )
        inventory = results.one()
        db.delete(inventory)
        db.commit()
        return inventory.id

    except Exception as e:
        print("EXCEPTION delete_inventory:", e)
        return None
