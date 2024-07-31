import os
from subscription.model import Subscription
from lib.payment_providers.razorpay import razorpay


RAZORPAY_MONTHLY_PLAN_ID = os.environ["RAZORPAY_MONTHLY_PLAN_ID"]


def create_razorpay_subscription(subscription: Subscription):
    # TODO plan id - create these when creating price
    # attach the price to the plan id
    razorpay_plan_id = RAZORPAY_MONTHLY_PLAN_ID
    razorpay_subscription = razorpay.subscription.create(
        {
            "plan_id": razorpay_plan_id,
            "customer_notify": 1,
            "quantity": 1,
            "total_count": 6,  # TODO
            # "start_at": subscription.start_date,
            "addons": [
                {
                    "item": {
                        "name": f"{sli.price.variant.product.name}: {sli.price.variant.name}",
                        "amount": sli.price.unit_amount * sli.quantity,
                        "currency": sli.price.currency,
                    }
                }
                for sli in subscription.line_items
            ],
            "notes": {
                "shop": subscription.shop_id,
                "customer": subscription.customer_id,
                "subscription": subscription.id,
            },
        }
    )
    subscription.razorpay_plan_id = razorpay_plan_id
    subscription.razorpay_subscription_id = razorpay_subscription["id"]
