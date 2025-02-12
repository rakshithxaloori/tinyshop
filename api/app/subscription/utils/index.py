from app.subscription.model import Subscription
from app.subscription import schema


def pydantify_subscriptions(rows: list[Subscription]) -> list[schema.Subscription]:
    subscriptions: list[schema.Subscription] = []
    for sub_ins in rows:
        subscriptions.append(
            schema.Subscription(
                **sub_ins.model_dump(
                    exclude={
                        "customer",
                        "customer_address",
                        "billing_cycle_anchor_config",
                        "pending_invoice_interval",
                        "cancellation_details",
                    }
                ),
                customer=sub_ins.customer_id,
                customer_address=sub_ins.customer_address_id,
                # TODO return variant?
                billing_cycle_anchor_config=schema.BillingCycleAnchorConfig(
                    **sub_ins.model_dump(
                        include={"day_of_month", "hour", "minute", "month", "second"}
                    )
                ),
                pending_invoice_interval=schema.PendingInvoiceInterval(
                    **sub_ins.model_dump(include={"interval", "interval_count"})
                ),
                cancellation_details=(
                    schema.CancellationDetails(
                        **sub_ins.model_dump(include={"review", "feedback", "reason"})
                    )
                ),
                provider_details=schema.ProviderDetails(
                    razorpay=(
                        schema.RazorpayDetails(
                            subscription_id=sub_ins.razorpay_subscription_id
                        )
                        if sub_ins.razorpay_subscription_id
                        else None
                    )
                ),
                line_items=[
                    schema.SubscriptionLineItem(
                        **sli.model_dump(exclude={"price"}), price=sli.price_id
                    )
                    for sli in sub_ins.line_items
                ]
            )
        )
    return subscriptions
