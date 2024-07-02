from warehouse.model import Warehouse, WarehouseAddress
from warehouse import schema


def pydantify_warehouses(
    rows: list[tuple[Warehouse, WarehouseAddress]]
) -> list[schema.Warehouse]:
    warehouses: list[Warehouse] = []
    for wh, wha in rows:
        warehouses.append(
            schema.Warehouse(
                wh.model_dump(exclude={"created", "updated"}),
                created=int(wh.created.timestamp()),
                updated=int(wh.updated.timestamp()),
                address=schema.WarehouseAddress(**wha.model_dump()),
            )
        )

    return warehouses
