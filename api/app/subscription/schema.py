from pydantic import BaseModel

from app.lib.model import PyBaseModel
from app.lib.object import ObjectType
from app.subscription.model import (
    CollectionMethodEnum,
    SubscriptionStatusEnum,
    SubscriptionCancellationDetailsFeedbackEnum,
    SubscriptionCancellationDetailsReasonEnum,
)
from app.price.enum import RecurringTypeEnum


class PendingInvoiceInterval(BaseModel):
    interval: RecurringTypeEnum
    interval_count: int


class BillingCycleAnchorConfig(BaseModel):
    day_of_month: int
    hour: int | None = None
    minute: int | None = None
    month: int | None = None
    second: int | None = None


class CancellationDetails(BaseModel):
    review: str | None = None
    feedback: SubscriptionCancellationDetailsFeedbackEnum | None = None
    reason: SubscriptionCancellationDetailsReasonEnum | None = None


class RazorpayDetails(BaseModel):
    subscription_id: str


class ProviderDetails(BaseModel):
    razorpay: RazorpayDetails | None = None


class SubscriptionLineItem(BaseModel):
    price: str
    quantity: int


class SubscriptionBase(BaseModel):
    cancel_at_period_end: bool
    collection_method: CollectionMethodEnum
    start_date: int
    billing_cycle_anchor: int
    cancel_at: int | None = None
    billing_cycle_anchor_config: BillingCycleAnchorConfig
    pending_invoice_interval: PendingInvoiceInterval
    customer: str
    customer_address: str | None = None
    line_items: list[SubscriptionLineItem]


class SubscriptionCreate(SubscriptionBase):
    checkout: str | None = None


class Subscription(PyBaseModel, SubscriptionBase):
    id: str
    object: str = ObjectType.SUBSCRIPTION
    current_period_end: int
    current_period_start: int
    status: SubscriptionStatusEnum
    canceled_at: int | None = None
    days_until_due: int | None = None
    ended_at: int | None = None
    start_date: int
    next_pending_invoice: int
    cancellation_details: CancellationDetails | None = None
    provider_details: ProviderDetails


class SubscriptionUpdate(BaseModel):
    status: SubscriptionStatusEnum | None = None
    cancel_at_period_end: bool | None = None
    collection_method: CollectionMethodEnum | None = None
    billing_cycle_anchor: int | None = None
    quantity: int | None = None
    billing_cycle_anchor_config: BillingCycleAnchorConfig | None = None
    pending_invoice_interval: PendingInvoiceInterval | None = None
    cancellation_details: CancellationDetails | None = None

    customer_address: str | None = None
    days_until_due: int | None = None


class SubscriptionList(BaseModel):
    object: str = "list"
    url: str = "/v1/subscriptions"
    has_more: bool
    data: list[Subscription] = []


class SubscriptionDelete(BaseModel):
    id: str
    object: str = ObjectType.SUBSCRIPTION
    deleted: bool
