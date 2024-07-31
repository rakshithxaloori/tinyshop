from checkout.model import Checkout
from checkout import schema
from subscription import schema as subs_schema
from subscription.utils.index import pydantify_subscriptions

from lib.limit import LIST_LIMIT_COUNT


def pydantify_checkouts(rows: list[Checkout]) -> list[schema.Checkout]:
    checkouts: list[schema.Checkout] = []
    # TODO add unpaid invoice or subscription to checkout, so they don't
    # have to fetch the invoices or subscriptions
    for ch_ins in rows:
        checkouts.append(
            schema.Checkout(
                **ch_ins.model_dump(exclude={"customer", "customer_address"}),
                customer=ch_ins.customer_id,
                customer_address=ch_ins.customer_address_id,
                subscriptions=(
                    subs_schema.SubscriptionList(
                        data=pydantify_subscriptions(
                            ch_ins.subscriptions[:LIST_LIMIT_COUNT]
                        ),  # TODO
                        has_more=False,
                        url=f"/v1/subscriptions?checkout={ch_ins.id}",
                    )
                    if ch_ins.subscriptions
                    else None
                ),
            )
        )
    return checkouts
