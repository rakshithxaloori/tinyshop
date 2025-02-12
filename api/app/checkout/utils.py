from app.checkout.model import Checkout
from app.checkout import schema
from app.subscription import schema as subs_schema
from app.subscription.utils.index import pydantify_subscriptions

from app.lib.limit import LIST_LIMIT_COUNT


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
                line_items=schema.CheckoutLineItemList(
                    data=[
                        schema.CheckoutLineItem(
                            price=line_item.price_id, quantity=line_item.quantity
                        )
                        for line_item in ch_ins.line_items[:LIST_LIMIT_COUNT]
                    ],
                    has_more=False,
                    url=f"/v1/checkout_items?checkout={ch_ins.id}",
                ),
            )
        )
    return checkouts
