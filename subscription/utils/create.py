from datetime import datetime
from sqlmodel import Session

from checkout.model import Checkout
from price.enum import PriceTypeEnum
from price.model import Price
from subscription.model import CollectionMethodEnum
from subscription import schema
from subscription import crud


def create_subscriptions_from_checkout(db: Session, checkout: Checkout):
    # Create subscriptions
    subscription_prices: list[tuple[Price, int]] = []
    for ci in checkout.cart.items:
        if ci.price.type == PriceTypeEnum.SUBSCRIPTION:
            subscription_prices.append((ci.price, ci.quantity))

    if len(subscription_prices) > 0:
        subs_groups: dict[str, list[tuple[Price, int]]] = {}
        for price, quantity in subscription_prices:
            # Group them by interval and interval count
            group_key = (price.interval, price.interval_count)
            if group_key not in subs_groups:
                subs_groups[group_key] = []
            subs_groups[group_key].append((price, quantity))

        for key, price_quantity_list in subs_groups.items():
            # Create a subscription
            interval, interval_count = key
            current_time = datetime.now()
            crud.create_subscription(
                checkout.shop_id,
                checkout.livemode,
                schema.SubscriptionCreate(
                    cancel_at_period_end=False,
                    collection_method=CollectionMethodEnum.COLLECT_AUTOMATICALLY,
                    start_date=int(current_time.timestamp()),
                    billing_cycle_anchor=int(current_time.timestamp()),
                    billing_cycle_anchor_config=schema.BillingCycleAnchorConfig(
                        day_of_month=current_time.day,
                        hour=current_time.hour,
                        minute=current_time.minute,
                        second=current_time.second,
                    ),
                    pending_invoice_interval=schema.PendingInvoiceInterval(
                        interval=interval,
                        interval_count=interval_count,
                    ),
                    customer=checkout.customer_id,
                    customer_address=checkout.customer_address_id,
                    line_items=[
                        schema.SubscriptionLineItem(price=price.id, quantity=quantity)
                        for price, quantity in price_quantity_list
                    ],
                    checkout=checkout.id,
                ),
                db,
                can_commit=False,
            )
