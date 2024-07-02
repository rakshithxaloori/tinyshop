from typing import Annotated
from fastapi import APIRouter, Depends, Form


from warehouse.inventory import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep


router = APIRouter(prefix="/v1/inventories")


def create_inventory_form(
    variant: Annotated[str, Form()],
    warehouse: Annotated[str, Form()],
    quantity: Annotated[int, Form()],
) -> schema.InventoryCreate:
    return schema.InventoryCreate(
        variant=variant,
        warehouse=warehouse,
        quantity=quantity,
    )


def update_inventory_form(quantity: Annotated[int, Form()]) -> schema.InventoryUpdate:
    return schema.InventoryUpdate(quantity=quantity)


@router.post("", response_model=schema.Inventory)
def create_inventory(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    inventory: Annotated[schema.InventoryCreate, Depends(create_inventory_form)],
):
    new_inventory = crud.create_inventory(
        x_shop_id,
        x_livemode,
        inventory,
    )
    return new_inventory


@router.post("/{inventory_id}", response_model=schema.Inventory)
def update_inventory(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    inventory_id: str,
    inventory: Annotated[schema.InventoryUpdate, Depends(update_inventory_form)],
):
    updated_inventory = crud.update_inventory(
        x_shop_id,
        x_livemode,
        inventory_id,
        inventory,
    )
    return updated_inventory


@router.delete("/{inventory_id}", response_model=schema.InventoryDelete)
def delete_inventory(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    inventory_id: str,
):
    deleted_id = crud.delete_inventory(
        x_shop_id,
        x_livemode,
        inventory_id,
    )
    return schema.InventoryDelete(
        id=inventory_id,
        deleted=deleted_id is not None,
    )
