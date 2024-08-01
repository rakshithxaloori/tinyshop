// Enums
type RecurringTypeEnum = "day" | "week" | "month" | "quarter" | "year";

type SubscriptionStatusEnum =
  | "incomplete"
  | "incomplete_expired"
  | "active"
  | "past_due"
  | "canceled"
  | "unpaid"
  | "paused"
  | "completed";

type CollectionMethodEnum = "collect_automatically" | "send_invoice";

type SubscriptionCancellationDetailsFeedbackEnum =
  | "customer_service"
  | "low_quality"
  | "missing_features"
  | "switched_service"
  | "too_complex"
  | "too_expensive"
  | "unused"
  | "other";

type SubscriptionCancellationDetailsReasonEnum =
  | "cancellation_requested"
  | "payment_disputed"
  | "payment_failed";

// Interfaces
interface PendingInvoiceInterval {
  interval: RecurringTypeEnum;
  interval_count: number;
}

interface BillingCycleAnchorConfig {
  day_of_month: number;
  hour?: number;
  minute?: number;
  month?: number;
  second?: number;
}

interface CancellationDetails {
  review?: string;
  feedback?: SubscriptionCancellationDetailsFeedbackEnum;
  reason?: SubscriptionCancellationDetailsReasonEnum;
}

interface RazorpayDetails {
  subscription_id: string;
}

interface ProviderDetails {
  razorpay?: RazorpayDetails;
}

interface SubscriptionLineItem {
  price: string;
  quantity: number;
}

interface SubscriptionBase {
  cancel_at_period_end: boolean;
  collection_method: CollectionMethodEnum;
  start_date: number;
  billing_cycle_anchor: number;
  cancel_at?: number;
  billing_cycle_anchor_config: BillingCycleAnchorConfig;
  pending_invoice_interval: PendingInvoiceInterval;
  customer: string;
  customer_address: string;
  line_items: SubscriptionLineItem[];
}

interface SubscriptionCreate extends SubscriptionBase {
  checkout?: string;
}

interface Subscription extends SubscriptionBase {
  id: string;
  object: "subscription";
  current_period_end: number;
  current_period_start: number;
  status: SubscriptionStatusEnum;
  canceled_at?: number;
  days_until_due?: number;
  ended_at?: number;
  start_date: number;
  next_pending_invoice: number;
  cancellation_details?: CancellationDetails;
  provider_details: ProviderDetails;
}

interface SubscriptionUpdate {
  status?: SubscriptionStatusEnum;
  cancel_at_period_end?: boolean;
  collection_method?: CollectionMethodEnum;
  billing_cycle_anchor?: number;
  quantity?: number;
  billing_cycle_anchor_config?: BillingCycleAnchorConfig;
  pending_invoice_interval?: PendingInvoiceInterval;
  cancellation_details?: CancellationDetails;
  customer_address?: string;
  days_until_due?: number;
}

interface SubscriptionList {
  object: "list";
  url: "/v1/subscriptions";
  has_more: boolean;
  data: Subscription[];
}

interface SubscriptionDelete {
  id: string;
  object: "subscription";
  deleted: boolean;
}

export type {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
  SubscriptionList,
  SubscriptionDelete,
};
