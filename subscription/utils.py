from subscription.model import Subscription
from subscription import schema


def pydantify_subscriptions(rows: list[Subscription]) -> list[schema.Subscription]:
    subscriptions: list[schema.Subscription] = []
    for sub_ins in rows:
        subscriptions.append(
            schema.Subscription(
                **sub_ins.model_dump(
                    exclude={
                        "created",
                        "updated",
                        "customer",
                        "customer_address",
                        "price",
                        "billing_cycle_anchor_config",
                        "pending_invoice_interval",
                        "cancellation_details",
                    }
                ),
                created=int(sub_ins.created.timestamp()),
                updated=int(sub_ins.updated.timestamp()),
                customer=sub_ins.customer_id,
                customer_address=sub_ins.customer_address_id,
                # TODO return variant?
                price=sub_ins.price_id,
                billing_cycle_anchor_config=schema.BillingCycleAnchorConfig(
                    **sub_ins.billing_cycle_anchor_config.model_dump()
                ),
                pending_invoice_interval=schema.PendingInvoiceInterval(
                    **sub_ins.pending_invoice_interval.model_dump()
                ),
                cancellation_details=(
                    schema.CancellationDetails(
                        **sub_ins.cancellation_details.model_dump()
                    )
                    if sub_ins.cancellation_details
                    else None
                )
            )
        )
    return subscriptions
