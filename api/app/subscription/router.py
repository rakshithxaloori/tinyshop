from sqlmodel import Session
from fastapi import APIRouter, Depends


from app.subscription import schema, crud
from app.lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from app.lib.session import get_session


router = APIRouter(prefix="/v1/subscriptions")


@router.post("", response_model=schema.Subscription)
def create_subscription(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    subscription: schema.SubscriptionCreate = FormDep(schema.SubscriptionCreate),
    db: Session = Depends(get_session),
):
    new_subs = crud.create_subscription(
        shop_id,
        livemode,
        subscription,
        db,
    )
    return new_subs


@router.post("/{subscription_id}", response_model=schema.Subscription)
def update_subscription(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    subscription_id: str,
    subscription: schema.SubscriptionUpdate = FormDep(schema.SubscriptionUpdate),
    db: Session = Depends(get_session),
):
    updated_subs = crud.update_subscription(
        shop_id,
        livemode,
        subscription_id,
        subscription,
        db,
    )
    return updated_subs


@router.get("/{subscription_id}", response_model=schema.Subscription)
def retrieve_subscription(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    subscription_id: str,
    db: Session = Depends(get_session),
):
    subs = crud.retrieve_subscription(
        shop_id,
        livemode,
        subscription_id,
        db,
    )
    return subs


@router.get("", response_model=schema.SubscriptionList)
def list_subscriptions(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    # TODO skip limit
    subs_list = crud.list_subscriptions(
        shop_id,
        livemode,
        db,
    )
    return subs_list


@router.delete("/{subscription_id}", response_model=schema.SubscriptionDelete)
def delete_subscription(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    subscription_id: str,
    db: Session = Depends(get_session),
):
    deleted_subs = crud.delete_subscription(
        shop_id,
        livemode,
        subscription_id,
        db,
    )
    return deleted_subs
