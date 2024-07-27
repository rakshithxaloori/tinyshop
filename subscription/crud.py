from datetime import datetime, timedelta
from sqlmodel import Session, select

from subscription.model import (
    Subscription,
    SubscriptionBillingCycleAnchorConfig,
    SubscriptionPendingInvoiceInterval,
    SubscriptionStatusEnum,
)
from customer.model import Customer
from user_address.model import UserAddress
from price.model import Price
from subscription.utils import pydantify_subscriptions
from lib.session import update_instance
from subscription import schema


def create_subscription(
    shop_id: str,
    livemode: bool,
    subscription: schema.SubscriptionCreate,
    db: Session,
) -> schema.Subscription | None:
    try:
        sub_data = subscription.model_dump(
            exclude={
                "customer",
                "customer_address",
                "price",
                "billing_cycle_anchor_config",
                "pending_invoice_interval",
            }
        )
        customer_res = db.exec(
            select(Customer.id)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == subscription.customer)
        )
        customer_id = customer_res.one()

        customer_addr_res = db.exec(
            select(UserAddress.id)
            .where(UserAddress.livemode == livemode)
            .where(UserAddress.id == subscription.customer_address)
        )
        cus_addr_id = customer_addr_res.one()

        price_res = db.exec(
            select(Price.id)
            .where(Price.shop_id == shop_id)
            .where(Price.livemode == livemode)
            .where(Price.id == subscription.price)
        )
        price_id = price_res.one()

        period_end = datetime.fromtimestamp(subscription.billing_cycle_anchor)
        config = subscription.billing_cycle_anchor_config
        while period_end <= datetime.now():
            # Move to the next cycle
            if config.month is not None:
                # Yearly cycle
                period_end = period_end.replace(year=period_end.year + 1)
            else:
                # Monthly cycle
                if period_end.month == 12:
                    period_end = period_end.replace(year=period_end.year + 1, month=1)
                else:
                    period_end = period_end.replace(month=period_end.month + 1)

            # Adjust day, hour, minute, second according to config
            period_end = period_end.replace(day=config.day_of_month)
            if config.hour is not None:
                period_end = period_end.replace(hour=config.hour)
            if config.minute is not None:
                period_end = period_end.replace(minute=config.minute)
            if config.second is not None:
                period_end = period_end.replace(second=config.second)

            # Handle cases where the day of month exceeds the days in the month
            while period_end.month != ((period_end - timedelta(days=1)).month + 1) % 12:
                period_end -= timedelta(days=1)

        period_end_timestamp = int(period_end.timestamp())
        next_pending_invoice = period_end_timestamp

        new_sub = Subscription(
            shop_id=shop_id,
            livemode=livemode,
            customer_id=customer_id,
            customer_address_id=cus_addr_id,
            price_id=price_id,
            status=SubscriptionStatusEnum.INCOMPLETE,
            start_date=subscription.billing_cycle_anchor,
            current_period_start=subscription.billing_cycle_anchor,
            current_period_end=period_end_timestamp,
            next_pending_invoice=next_pending_invoice,
            **sub_data,
        )
        db.add(new_sub)
        new_bca_config = SubscriptionBillingCycleAnchorConfig(
            livemode=livemode,
            subscription_id=new_sub.id,
            **subscription.billing_cycle_anchor_config.model_dump(),
        )
        db.add(new_bca_config)
        new_pii = SubscriptionPendingInvoiceInterval(
            livemode=livemode,
            subscription_id=new_sub.id,
            **subscription.pending_invoice_interval.model_dump(),
        )
        db.add(new_pii)

        db.commit()
        db.refresh(new_sub)
        py_subs = pydantify_subscriptions([new_sub])
        return py_subs.pop()

    except Exception as e:
        print("EXCEPTION create_subscription:", e)
        return None


def update_subscription(
    shop_id: str,
    livemode: bool,
    subscription_id: str,
    subscription: schema.SubscriptionUpdate,
    db: Session,
) -> schema.Subscription | None:
    try:
        data = subscription.model_dump(
            exclude_none=True,
            exclude={
                "customer_address",
                "billing_cycle_anchor_config",
                "pending_invoice_interval",
                "cancellation_details",
            },
        )

        sub_res = db.exec(
            select(Subscription)
            .where(Subscription.shop_id == shop_id)
            .where(Subscription.livemode == livemode)
            .where(Subscription.id == subscription_id)
        )
        sub_ins = sub_res.one()

        if subscription.customer_address:
            customer_addr_res = db.exec(
                select(UserAddress.id)
                .where(UserAddress.livemode == livemode)
                .where(UserAddress.id == subscription.customer_address)
            )
            cus_addr_id = customer_addr_res.one()
            sub_ins.customer_address_id = cus_addr_id

        update_instance(db, data, sub_ins)
        if subscription.billing_cycle_anchor_config:
            update_instance(
                db,
                subscription.billing_cycle_anchor_config.model_dump(),
                sub_ins.billing_cycle_anchor_config,
            )
        if subscription.pending_invoice_interval:
            update_instance(
                db,
                subscription.pending_invoice_interval.model_dump(),
                sub_ins.pending_invoice_interval,
            )
        # TODO create a cancellation_details if it doesn't exist
        # TODO test creation and update
        if subscription.cancellation_details:
            update_instance(
                db,
                subscription.cancellation_details.model_dump(),
                sub_ins.cancellation_details,
            )

        db.commit()
        db.refresh(sub_ins)
        py_subs = pydantify_subscriptions([sub_ins])
        return py_subs.pop()

    except Exception as e:
        print("EXCEPTION update_subscription:", e)
        return None


def retrieve_subscription(
    shop_id: str,
    livemode: bool,
    subscription_id: str,
    db: Session,
) -> schema.Subscription | None:
    try:

        sub_res = db.exec(
            select(Subscription)
            .where(Subscription.shop_id == shop_id)
            .where(Subscription.livemode == livemode)
            .where(Subscription.id == subscription_id)
        )
        sub_ins = sub_res.one()
        py_subs = pydantify_subscriptions([sub_ins])
        return py_subs.pop()
    except Exception as e:
        print("EXCEPTION retrieve_subscription:", e)
        return None


def list_subscriptions(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.SubscriptionList:
    results = db.exec(
        select(Subscription)
        .where(Subscription.shop_id == shop_id)
        .where(Subscription.livemode == livemode)
        .offset(skip)
        .limit(limit)
    )
    rows = list(results.all())
    subs = pydantify_subscriptions(rows)
    return schema.SubscriptionList(
        has_more=False,  # TODO
        data=subs,
    )


def delete_subscription(
    shop_id: str,
    livemode: bool,
    subscription_id: str,
    db: Session,
) -> schema.SubscriptionDelete | None:
    try:

        sub_res = db.exec(
            select(Subscription)
            .where(Subscription.shop_id == shop_id)
            .where(Subscription.livemode == livemode)
            .where(Subscription.id == subscription_id)
        )
        sub_ins = sub_res.one()
        db.delete(sub_ins)
        db.commit()
        return schema.SubscriptionDelete(
            id=sub_ins.id,
            deleted=True,
        )
    except Exception as e:
        print("EXCEPTION delete_subscription:", e)
        return schema.SubscriptionDelete(
            id=subscription_id,
            deleted=False,
        )
