from price.model import Price, PriceTypeEnum
from price import schema


def pydantify_prices(rows: list[Price]) -> list[schema.Price]:
    prices: list[schema.Price] = []
    for price in rows:
        price_data = price.model_dump(
            exclude={"customer_unit_amount", "recurring", "variant"}
        )
        prices.append(
            schema.Price(
                **price_data,
                variant=price.variant_id,
                product=price.variant.product_id,
                customer_unit_amount=(
                    schema.CustomerUnitAmount(
                        **price.model_dump(include={"maximum", "minimum", "preset"})
                    )
                ),
                recurring=(
                    (
                        schema.Recurring(
                            **price.model_dump(include={"interval", "interval_count"})
                        )
                    )
                    if price.type == PriceTypeEnum.SUBSCRIPTION
                    else None
                )
            )
        )

    return prices
