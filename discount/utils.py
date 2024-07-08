from discount.model import Discount
from discount import schema
from customer import schema as cus_schema


def pydantify_discounts(rows: list[Discount]) -> list[schema.Discount]:
    discounts: list[schema.Discount] = []
    for row in rows:
        schema.Discount(
            **row.model_dump(exclude={"created", "updated"}),
            created=int(row.created.timestamp()),
            updated=int(row.updated.timestamp()),
            customers=schema.DiscountCustomers(
                data=[
                    cus_schema.Customer(**cus.model_dump())
                    for cus in row.customers_select
                ],
                url=f"/v1/discounts/{row.id}/customers",
                has_more=False,  # TODO
            ),
        )

    return discounts
