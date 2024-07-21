// Interface for InvoiceCustomerAddress
interface InvoiceCustomerAddress {
  line1: string;
  line2?: string | null;
  city: string;
  state: string;
  country: string;
  postal_code: string;
}

// Base interface for Invoice
interface InvoiceBase {
  amount_paid: number;
  due_date: number;
  status: "draft" | "open" | "paid" | "uncollectible" | "void";
}

// Interface for InvoiceCreate
interface InvoiceCreate extends InvoiceBase {
  checkout?: string | null;
  subscriptions: string[];
}

// Interface for Invoice
interface Invoice extends InvoiceBase {
  id: string;
  object: "invoice";
  amount_remaining: number;
  amount_shipping: number;
  amount_tax: number;
  amount_subtotal: number;
  amount_total: number;
  amount_discount: number;
  currency: string;
  attempt_count: number;
  attempted: boolean;
  invoice_pdf?: string | null;
  paid: boolean;
  customer: string;
  checkout: string;
  subscriptions: string[];
  customer_address: InvoiceCustomerAddress;
}

// Interface for InvoiceList
interface InvoiceList {
  object: string;
  data: Invoice[];
  has_more: boolean;
  url: string;
}

// Interface for InvoiceUpdate
interface InvoiceUpdate {
  attempt_count?: number | null;
  attempted?: boolean | null;
  amount_paid?: number | null;
  amount_remaining?: number | null;
  due_date?: number | null;
}

// Interface for InvoiceDelete
interface InvoiceDelete {
  id: string;
  object: string;
  deleted: boolean;
}

export { Invoice, InvoiceCreate, InvoiceUpdate, InvoiceList, InvoiceDelete };
