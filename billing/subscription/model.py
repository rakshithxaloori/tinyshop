import enum
from sqlalchemy import Column, Text, ForeignKey, Enum, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship


from utils.model import SqlBase
from utils.primary_key import get_primary_key


class SubscriptionStatusEnum(str, enum.Enum):
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    PAUSED = "paused"


class CollectionMethodEnum(str, enum.Enum):
    COLLECT_AUTOMATICALLY = "collect_automatically"
    SEND_INVOICE = "send_invoice"


class Subscription(SqlBase):
    __tablename__ = "subscription"

    id = Column(Text, primary_key=True, default=get_primary_key("sub"))
    cancel_at_period_end = Column(Boolean)
    current_period_end = Column(DateTime)
    current_period_start = Column(DateTime)
    status = Column(Enum(SubscriptionStatusEnum))
    collection_method = Column(Enum(CollectionMethodEnum))
    billing_cycle_anchor = Column(DateTime)
    cancel_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    days_until_due = Column(Integer, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    start_date = Column(DateTime)

    customer_id = Column(Text, ForeignKey("customer.id", ondelete="CASCADE"))
    customer = relationship("Customer", back_populates="subscriptions")
    variant_id = Column(Text, ForeignKey("variant.id", ondelete="CASCADE"))
    variant = relationship("Variant", back_populates="subscriptions")
    billing_cycle_anchor_config_id = Column(
        Text, ForeignKey("_subscription_billing_cycle_anchor_config.id"), nullable=True
    )
    billing_cycle_anchor_config = relationship(
        "SubscriptionBillingCycleAnchorConfig", back_populates="subscription"
    )
    cancellation_details_id = Column(
        Text, ForeignKey("_subscription_cancellation_details.id"), nullable=True
    )
    cancellation_details = relationship(
        "SubscriptionCancellationDetails", back_populates="subscription"
    )


class SubscriptionBillingCycleAnchorConfig(SqlBase):
    __tablename__ = "_subscription_billing_cycle_anchor_config"

    id = Column(Text, primary_key=True, default=get_primary_key("_sbcac"))
    day_of_month = Column(Integer)
    hour = Column(Integer, nullable=True)
    minute = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    second = Column(Integer, nullable=True)

    subscription_id = Column(Text, ForeignKey("subscription.id", ondelete="CASCADE"))


class SubscriptionCancellationDetailsFeedbackEnum(str, enum.Enum):
    customer_service = "customer_service"
    low_quality = "low_quality"
    missing_features = "missing_features"
    switched_service = "switched_service"
    too_complex = "too_complex"
    too_expensive = "too_expensive"
    unused = "unused"
    other = "other"


class SubscriptionCancellationDetailsReasonEnum(str, enum.Enum):
    cancellation_requested = "cancellation_requested"
    payment_disputed = "payment_disputed"
    payment_failed = "payment_failed"


class SubscriptionCancellationDetails(SqlBase):
    __tablename__ = "_subscription_cancellation_details"

    id = Column(Text, primary_key=True, default=get_primary_key("_scd"))
    comment = Column(Text, nullable=True)
    feedback = Column(Enum(SubscriptionCancellationDetailsFeedbackEnum), nullable=True)
    reason = Column(Enum(SubscriptionCancellationDetailsReasonEnum), nullable=True)

    subscription_id = Column(Text, ForeignKey("subscription.id", ondelete="CASCADE"))
