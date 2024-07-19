from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from subscription.model import (
    CollectionMethodEnum,
    SubscriptionStatusEnum,
    SubscriptionPendingInvoiceIntervalEnum,
    SubscriptionCancellationDetailsFeedbackEnum,
    SubscriptionCancellationDetailsReasonEnum,
)


class PendingInvoiceInterval(BaseModel):
    interval: SubscriptionPendingInvoiceIntervalEnum
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


class SubscriptionBase(BaseModel):
    cancel_at_period_end: bool
    collection_method: CollectionMethodEnum
    billing_cycle_anchor: int
    cancel_at: int | None = None
    quantity: int
    billing_cycle_anchor_config: BillingCycleAnchorConfig
    pending_invoice_interval: PendingInvoiceInterval
    cancellation_details: CancellationDetails


class SubscriptionCreate(SubscriptionBase):
    customer: str
    customer_address: str
    price: str


class Subscription(PyBaseModel, SubscriptionBase):
    id: str
    object: str = ObjectType.SUBSCRIPTION
    customer: str
    customer_address: str
    price: str
    current_period_end: int
    current_period_start: int
    status: SubscriptionStatusEnum
    canceled_at: int | None = None
    days_until_due: int | None = None
    ended_at: int | None = None
    start_date: int | None = None
    next_pending_invoice: int


class SubscriptionUpdate(BaseModel):
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
