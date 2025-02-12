from app.inventory.model import Inventory
from app.inventory import schema


def pydantify_inventories(rows: list[Inventory]) -> list[schema.Inventory]:
    inventories: list[schema.Inventory] = []
    for row in rows:
        inventories.append(
            schema.Inventory(
                **row.model_dump(
                    exclude={
                        "variant",
                        "warehouse",
                    }
                ),
                warehouse=row.warehouse_id,
                variant=row.variant_id,
            )
        )

    return inventories
