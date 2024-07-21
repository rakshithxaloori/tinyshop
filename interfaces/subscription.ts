// Enum for SubscriptionStatusEnum
type SubscriptionStatusEnum =
  | "incomplete"
  | "incomplete_expired"
  | "active"
  | "past_due"
  | "canceled"
  | "unpaid"
  | "paused";

// Enum for CollectionMethodEnum
type CollectionMethodEnum = "collect_automatically" | "send_invoice";

// Enum for SubscriptionPendingInvoiceIntervalEnum
type SubscriptionPendingInvoiceIntervalEnum = "day" | "week" | "month" | "year";

// Enum for SubscriptionCancellationDetailsFeedbackEnum
type SubscriptionCancellationDetailsFeedbackEnum =
  | "customer_service"
  | "low_quality"
  | "missing_features"
  | "switched_service"
  | "too_complex"
  | "too_expensive"
  | "unused"
  | "other";

// Enum for SubscriptionCancellationDetailsReasonEnum
type SubscriptionCancellationDetailsReasonEnum =
  | "cancellation_requested"
  | "payment_disputed"
  | "payment_failed";

// Interface for PendingInvoiceInterval
interface PendingInvoiceInterval {
  interval: SubscriptionPendingInvoiceIntervalEnum;
  interval_count: number;
}

// Interface for BillingCycleAnchorConfig
interface BillingCycleAnchorConfig {
  day_of_month: number;
  hour?: number | null;
  minute?: number | null;
  month?: number | null;
  second?: number | null;
}

// Interface for CancellationDetails
interface CancellationDetails {
  review?: string | null;
  feedback?: SubscriptionCancellationDetailsFeedbackEnum | null;
  reason?: SubscriptionCancellationDetailsReasonEnum | null;
}

// Base interface for Subscription
interface SubscriptionBase {
  cancel_at_period_end: boolean;
  collection_method: CollectionMethodEnum;
  billing_cycle_anchor: number;
  cancel_at?: number | null;
  quantity: number;
  billing_cycle_anchor_config: BillingCycleAnchorConfig;
  pending_invoice_interval: PendingInvoiceInterval;
}

// Interface for SubscriptionCreate
interface SubscriptionCreate extends SubscriptionBase {
  customer: string;
  customer_address: string;
  price: string;
}

// Interface for Subscription
interface Subscription extends SubscriptionBase {
  id: string;
  object: string;
  customer: string;
  customer_address: string;
  price: string;
  current_period_end: number;
  current_period_start: number;
  status: SubscriptionStatusEnum;
  canceled_at?: number | null;
  days_until_due?: number | null;
  ended_at?: number | null;
  start_date?: number | null;
  next_pending_invoice: number;
  cancellation_details?: CancellationDetails | null;
}

// Interface for SubscriptionUpdate
interface SubscriptionUpdate {
  cancel_at_period_end?: boolean | null;
  collection_method?: CollectionMethodEnum | null;
  billing_cycle_anchor?: number | null;
  quantity?: number | null;
  billing_cycle_anchor_config?: BillingCycleAnchorConfig | null;
  pending_invoice_interval?: PendingInvoiceInterval | null;
  cancellation_details?: CancellationDetails | null;
  customer_address?: string | null;
  days_until_due?: number | null;
}

// Interface for SubscriptionList
interface SubscriptionList {
  object: string;
  url: string;
  has_more: boolean;
  data: Subscription[];
}

// Interface for SubscriptionDelete
interface SubscriptionDelete {
  id: string;
  object: string;
  deleted: boolean;
}

export {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
  SubscriptionList,
  SubscriptionDelete,
};
