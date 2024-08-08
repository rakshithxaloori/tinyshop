from sqlmodel import select

from app.celery import celery_app
from app.checkout.model import Checkout
from app.subscription.utils.create import create_subscriptions_from_checkout
from app.lib.session import create_task_session


@celery_app.task
def create_subscriptions_task(shop_id: str, livemode: bool, checkout_id: str):
    with create_task_session() as db:
        ch_res = db.exec(
            select(Checkout)
            .where(Checkout.shop_id == shop_id)
            .where(Checkout.livemode == livemode)
            .where(Checkout.id == checkout_id)
        )
        checkout = ch_res.one()
        create_subscriptions_from_checkout(db, checkout)
        # A commit already happens in create_subscriptions_from_checkout
        # TODO can we only commit once in every session?
        # TODO create invoices
