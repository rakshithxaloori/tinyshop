from sqlmodel import Session
from fastapi import APIRouter, Depends


from app.inventory import schema, crud
from app.lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from app.lib.session import get_session


router = APIRouter(prefix="/v1/inventory")


@router.post("", response_model=schema.Inventory)
def create_inventory(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    inventory: schema.InventoryCreate = FormDep(schema.InventoryCreate),
    db: Session = Depends(get_session),
):
    new_inventory = crud.create_inventory(
        shop_id,
        livemode,
        inventory,
        db,
    )
    return new_inventory


@router.post("/{inventory_id}", response_model=schema.Inventory)
def update_inventory(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    inventory_id: str,
    inventory: schema.InventoryUpdate = FormDep(schema.InventoryUpdate),
    db: Session = Depends(get_session),
):
    inventory = crud.update_inventory(
        shop_id,
        livemode,
        inventory_id,
        inventory,
        db,
    )
    return inventory


@router.delete("/{inventory_id}", response_model=schema.InventoryDelete)
def delete_inventory(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    inventory_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_inventory(
        shop_id,
        livemode,
        inventory_id,
        db,
    )
    return schema.InventoryDelete(
        id=inventory_id,
        deleted=deleted_id is not None,
    )
