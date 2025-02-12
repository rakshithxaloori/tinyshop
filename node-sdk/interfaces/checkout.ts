import { SubscriptionList } from "./subscription";

type CHECKOUT_OBJECT = "checkout";

// Enums
type CheckoutStatusEnum =
  | "open"
  | "complete"
  | "expired"
  | "canceled"
  | "abandoned";

// Interfaces
interface CheckoutLineItem {
  price: string;
  quantity: number;
}

interface CheckoutLineItemList {
  object: "list";
  data: CheckoutLineItem[];
  has_more: boolean;
  url: "/v1/checkouts/items";
}

interface CheckoutBase {
  return_url: string;
  success_url: string;
  url: string;
  customer_address?: string | null;
}

interface CheckoutCreate extends CheckoutBase {
  customer: string;
  cart: string;
}

interface Checkout extends CheckoutBase {
  id: string;
  object: CHECKOUT_OBJECT;
  status: CheckoutStatusEnum;
  currency: string;
  amount_total: number;
  amount_subtotal: number;
  amount_discount: number;
  amount_shipping: number;
  amount_tax: number;
  expires_at: number;
  customer: string;
  // invoice?: string | null;
  subscriptions?: SubscriptionList | null;
  line_items: CheckoutLineItemList;
}

interface CheckoutUpdate {
  customer_address?: string | null;
}

interface CheckoutList {
  object: "list";
  data: Checkout[];
  has_more: boolean;
  url: "/v1/checkouts";
}

interface CheckoutDelete {
  id: string;
  object: CHECKOUT_OBJECT;
  deleted: boolean;
}

export type {
  Checkout,
  CheckoutCreate,
  CheckoutUpdate,
  CheckoutList,
  CheckoutDelete,
};
