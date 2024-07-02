from warehouse.inventory.model import Inventory
from warehouse.inventory import schema


def pydantify_inventories(rows: list[Inventory]) -> list[schema.Inventory]:
    # Create, Update, Delete only
    inventories: list[schema.Inventory] = []
    for row in rows:
        inventories.append(
            schema.Inventory(
                row.model_dump(exclude={"created", "updated"}),
                created=int(row.created.timestamp()),
                updated=int(row.updated.timestamp()),
            )
        )

    return inventories
