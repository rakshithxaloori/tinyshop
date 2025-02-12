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

interface PendingInvoiceInterval {
  interval: RecurringTypeEnum;
  interval_count: number;
}

interface BillingCycleAnchorConfig {
  day_of_month: number;
  hour?: number | null;
  minute?: number | null;
  month?: number | null;
  second?: number | null;
}

interface CancellationDetails {
  review?: string | null;
  feedback?: SubscriptionCancellationDetailsFeedbackEnum | null;
  reason?: SubscriptionCancellationDetailsReasonEnum | null;
}

interface RazorpayDetails {
  subscription_id: string;
}

interface ProviderDetails {
  razorpay?: RazorpayDetails | null;
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
  cancel_at?: number | null;
  billing_cycle_anchor_config: BillingCycleAnchorConfig;
  pending_invoice_interval: PendingInvoiceInterval;
  customer: string;
  customer_address: string;
  line_items: SubscriptionLineItem[];
}

interface SubscriptionCreate extends SubscriptionBase {
  checkout?: string | null;
}

interface Subscription extends SubscriptionBase {
  id: string;
  object: "list";
  current_period_end: number;
  current_period_start: number;
  status: SubscriptionStatusEnum;
  canceled_at?: number | null;
  days_until_due?: number | null;
  ended_at?: number | null;
  start_date: number;
  next_pending_invoice: number;
  cancellation_details?: CancellationDetails | null;
  provider_details: ProviderDetails;
}

interface SubscriptionUpdate {
  status?: SubscriptionStatusEnum | null;
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

interface SubscriptionList {
  object: "list";
  url: string;
  has_more: boolean;
  data: Subscription[];
}

interface SubscriptionDelete {
  id: string;
  object: "list";
  deleted: boolean;
}

export type {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
  SubscriptionList,
  SubscriptionDelete,
};
