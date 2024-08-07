from warehouse.model import Warehouse
from warehouse import schema


def pydantify_warehouses(rows: list[Warehouse]) -> list[schema.Warehouse]:
    warehouses: list[schema.Warehouse] = []
    for wh in rows:
        warehouses.append(
            schema.Warehouse(
                **wh.model_dump(),
                address=schema.WarehouseAddress(
                    **wh.model_dump(
                        include={
                            "line1",
                            "line2",
                            "city",
                            "state",
                            "country",
                            "postal_code",
                        }
                    )
                ),
            )
        )

    return warehouses
