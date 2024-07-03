from typing import Annotated
from fastapi import Form


from warehouse.inventory import schema


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
