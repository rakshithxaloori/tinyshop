from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from inventory import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/inventories")


@router.post("", response_model=schema.Inventory)
def create_inventory(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    inventory: Annotated[schema.InventoryCreate, Depends(form.create_inventory_form)],
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
    inventory: Annotated[schema.InventoryUpdate, Depends(form.update_inventory_form)],
    db: Session = Depends(get_session),
):
    updated_inventory = crud.update_inventory(
        shop_id,
        livemode,
        inventory_id,
        inventory,
        db,
    )
    return updated_inventory


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
