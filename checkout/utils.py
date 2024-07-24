from checkout.model import Checkout
from checkout import schema


def pydantify_checkouts(rows: list[Checkout]) -> list[schema.Checkout]:
    checkouts: list[schema.Checkout] = []
    for ch_ins in rows:
        checkouts.append(
            schema.Checkout(
                **ch_ins.model_dump(exclude={"customer", "customer_address"}),
                customer=ch_ins.customer_id,
                customer_address=ch_ins.customer_address_id
            )
        )
    return checkouts
