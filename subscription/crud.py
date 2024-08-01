from sqlmodel import Session, select

from subscription.model import (
    Subscription,
    SubscriptionStatusEnum,
    SubscriptionLineItem,
)
from customer.model import Customer
from user_address.model import UserAddress
from price.model import Price
from subscription.utils.index import pydantify_subscriptions
from lib.session import update_instance
from subscription import schema
from shop.model import Shop
from lib.datetime import calculate_current_period_end
from checkout.model import Checkout
from subscription.utils.razorpay import create_razorpay_subscription
from lib.enum import PaymentsProviderEnum


def create_subscription(
    shop_id: str,
    livemode: bool,
    subscription: schema.SubscriptionCreate,
    db: Session,
    can_commit: bool = True,
) -> schema.Subscription | None:
    try:
        shop_payments_prov_res = db.exec(
            select(Shop.default_payments_provider)
            .where(Shop.id == shop_id)
            .where(Shop.livemode == livemode)
        )
        shop_payments_provider = shop_payments_prov_res.one()
        sub_data = subscription.model_dump(
            exclude={
                "checkout",
                "customer",
                "customer_address",
                "billing_cycle_anchor_config",
                "pending_invoice_interval",
                "line_items",
            }
        )

        if subscription.checkout:
            checkout_res = db.exec(
                select(Checkout.id)
                .where(Checkout.shop_id == shop_id)
                .where(Checkout.livemode == livemode)
                .where(Checkout.id == subscription.checkout)
            )
            _ = checkout_res.one()

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

        prices_res = db.exec(
            select(Price)
            .where(Price.shop_id == shop_id)
            .where(Price.livemode == livemode)
            .where(Price.id.in_([li.price for li in subscription.line_items]))
        )
        prices = list(prices_res.all())
        if len(prices) != subscription.line_items:
            # TODO throw error
            pass

        prices_amount_dict: dict[str, int] = {}
        for price in prices:
            prices_amount_dict[price.id] = price.unit_amount

        prices_quantity_dict: dict[str, int] = {}
        for li in subscription.line_items:
            prices_quantity_dict[li.price] = li.quantity

        current_period_end = calculate_current_period_end(
            subscription.start_date,
            subscription.pending_invoice_interval.interval,
            subscription.pending_invoice_interval.interval_count,
        )

        new_sub = Subscription(
            shop_id=shop_id,
            livemode=livemode,
            customer_id=customer_id,
            customer_address_id=cus_addr_id,
            status=SubscriptionStatusEnum.INCOMPLETE,
            current_period_start=subscription.start_date,
            current_period_end=current_period_end,
            next_pending_invoice=current_period_end,
            provider=shop_payments_provider,
            checkout_id=subscription.checkout if subscription.checkout else None,
            **sub_data,
            **subscription.billing_cycle_anchor_config.model_dump(),
            **subscription.pending_invoice_interval.model_dump(),
        )
        db.add(new_sub)

        for line_item in subscription.line_items:
            new_sli = SubscriptionLineItem(
                livemode=livemode,
                subscription_id=new_sub.id,
                price_id=line_item.price,
                quantity=line_item.quantity,
            )
            db.add(new_sli)

        # Create external subscriptions
        amount_subtotal = 0
        for price_id, unit_amount in prices_amount_dict.items():
            amount_subtotal += unit_amount * prices_quantity_dict[price_id]
        if shop_payments_provider == PaymentsProviderEnum.RAZORPAY:
            create_razorpay_subscription(new_sub, amount_subtotal)
            # Creates an UPDATE statement
            db.add(new_sub)

        # TODO Create an invoice

        if can_commit:
            db.commit()
            db.refresh(new_sub)
            py_subs = pydantify_subscriptions([new_sub])
            return py_subs.pop()
        return None

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
        # TODO handle cancel
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
