import os
from subscription.model import Subscription
from lib.payment_providers.razorpay import razorpay


RAZORPAY_MONTHLY_PLAN_ID = os.environ["RAZORPAY_MONTHLY_PLAN_ID"]


def create_razorpay_subscription(subscription: Subscription, amount_subtotal: int):
    razorpay_plan = razorpay.plan.create(
        {
            "period": f"{subscription.interval.value}ly",
            "interval": subscription.interval_count,
            "item": {
                "name": "Test plan - Weekly",
                "amount": amount_subtotal,
                "currency": "INR",  # TODO
                "description": "Description for the test plan",
            },
            "notes": {
                "shop": subscription.shop_id,
                "customer": subscription.customer_id,
                "subscription": subscription.id,
            },
        }
    )
    razorpay_subscription = razorpay.subscription.create(
        {
            "plan_id": razorpay_plan["id"],
            "customer_notify": 1,
            "quantity": 1,
            "total_count": 6,  # TODO
            # "start_at": subscription.start_date,
            "notes": {
                "shop": subscription.shop_id,
                "customer": subscription.customer_id,
                "subscription": subscription.id,
            },
        }
    )
    subscription.razorpay_plan_id = razorpay_plan["id"]
    subscription.razorpay_subscription_id = razorpay_subscription["id"]
