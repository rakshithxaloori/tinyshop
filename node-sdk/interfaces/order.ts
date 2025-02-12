// Enum for OrderTypeEnum
type OrderTypeEnum = "preorder" | "deferred" | "normal";

// Enum for OrderStatusEnum
type OrderStatusEnum =
  | "requires_inventory"
  | "requires_shipping"
  | "shipping"
  | "completed"
  | "return_requested";

// Interface for OrderLineItemCreate
interface OrderLineItemCreate {
  quantity: number;
  price: string;
}

// Interface for OrderLineItem
interface OrderLineItem {
  quantity: number;
  unit_amount: number;
  price: string;
}

// Base interface for Order
interface OrderBase {
  invoice?: string | null;
  customer: string;
}

// Interface for OrderCreate
interface OrderCreate extends OrderBase {
  line_items: OrderLineItemCreate[];
}

// Interface for Order
interface Order extends OrderBase {
  id: string;
  object: "list";
  number: number;
  status: OrderStatusEnum;
  type: OrderTypeEnum;
  line_items: OrderLineItem[];
}

// Interface for OrderList
interface OrderList {
  object: "list";
  url: string;
  data: Order[];
  has_more: boolean;
}

// Interface for OrderUpdate
interface OrderUpdate {
  type?: OrderTypeEnum | null;
  status?: OrderStatusEnum | null;
}

// Interface for OrderDelete
interface OrderDelete {
  id: string;
  object: "list";
  deleted: boolean;
}

export type { Order, OrderCreate, OrderUpdate, OrderList, OrderDelete };
