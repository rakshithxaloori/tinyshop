from checkout.model import Checkout
from checkout import schema


def pydantify_checkouts(rows: list[Checkout]) -> list[schema.Checkout]:
    checkouts: list[schema.Checkout] = []
    for ch_ins in rows:
        checkouts.append(
            schema.Checkout(
                **ch_ins.model_dump(exclude={"created", "updated"}),
                created=int(ch_ins.created.timestamp()),
                updated=int(ch_ins.updated.timestamp())
            )
        )
    return checkouts
