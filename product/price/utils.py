from product.price.model import Price, CustomerUnitAmount, Recurring
from product.price import schema


def pydantify_prices(
    rows: list[tuple[Price, CustomerUnitAmount, Recurring]]
) -> list[schema.Price]:
    prices: list[schema.Price] = []
    for price, cua, recurring in rows:
        price_data = price.model_dump(
            exclude={"created", "updated", "customer_unit_amount", "recurring"}
        )
        cua_data = cua.model_dump()
        recurring = recurring.model_dump()
        prices.append(
            schema.Price(
                **price_data,
                created=int(price.created.timestamp()),
                updated=int(price.updated.timestamp()),
                customer_unit_amount=schema.CustomerUnitAmount(**cua_data),
                recurring=schema.Recurring(**recurring)
            )
        )

    return prices
