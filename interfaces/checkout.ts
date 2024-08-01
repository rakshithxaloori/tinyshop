// Base interface for Checkout
interface CheckoutBase {
  return_url: string;
  success_url: string;
  url: string;
}

// Interface for CheckoutCreate
interface CheckoutCreate extends CheckoutBase {
  customer: string;
  customer_address?: string | null;
  cart: string;
}

// Interface for Checkout
interface Checkout extends CheckoutBase {
  id: string;
  object: string;
  status: "open" | "abandoned" | "complete" | "expired" | "processing";
  amount_total: number;
  amount_subtotal: number;
  amount_discount: number;
  amount_shipping: number;
  amount_tax: number;
  expires_at: number;
  customer: string;
  customer_address?: string | null;
  invoice?: string | null;
}

// Interface for CheckoutUpdate
interface CheckoutUpdate {
  status?: "open" | "abandoned" | "complete" | "expired" | "processing";
  customer_address?: string | null;
}

// Interface for CheckoutList
interface CheckoutList {
  object: string;
  data: Checkout[];
  has_more: boolean;
  url: string;
}

// Interface for CheckoutDelete
interface CheckoutDelete {
  id: string;
  object: string;
  deleted: boolean;
}

export type {
  Checkout,
  CheckoutCreate,
  CheckoutUpdate,
  CheckoutList,
  CheckoutDelete,
};
