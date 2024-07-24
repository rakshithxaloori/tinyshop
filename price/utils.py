from price.model import Price, CustomerUnitAmount, Recurring
from price import schema


def pydantify_prices(
    rows: list[tuple[Price, CustomerUnitAmount, Recurring]]
) -> list[schema.Price]:
    prices: list[schema.Price] = []
    for price, cua, recurring in rows:
        price_data = price.model_dump(exclude={"customer_unit_amount", "recurring"})
        prices.append(
            schema.Price(
                **price_data,
                customer_unit_amount=(
                    schema.CustomerUnitAmount(**cua.model_dump()) if cua else None
                ),
                recurring=(
                    schema.Recurring(**recurring.model_dump()) if recurring else None
                )
            )
        )

    return prices
