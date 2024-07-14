import { ObjectType } from "../utils/enum";
import { Product } from "./product";
import { Variant } from "./variant";

enum DiscountTypeEnum {
  OFF_PRODUCT = "off_product",
  OFF_ORDER = "off_order",
  SHIPPING = "shipping",
  BUY_X_GET_Y = "buy_x_get_y",
}

interface DiscountBase {
  type: DiscountTypeEnum;
  code: string;
  active: boolean;
  expires_at?: Date | null;
  applies_max?: number | null;
}

interface DiscountProductsList {
  object: string;
  url: string;
  has_more: boolean;
  data: (Product | string)[];
}

// TODO after adding customers to SDK
// interface DiscountCustomersList {
//   object: string;
//   url: string;
//   has_more: boolean;
//   data: (Customer | string)[];
// }

interface OffProduct {
  quantity_min?: number | null;
  amount_off?: number | null;
  percentage_off?: number | null;
  products?: DiscountProductsList | null;
}

interface OffProductUpdateProducts {
  add: string[];
  remove: string[];
}

interface OffProductUpdate {
  quantity_min?: number | null;
  amount_off?: number | null;
  percentage_off?: number | null;
  products?: OffProductUpdateProducts | null;
}

interface OffOrder {
  quantity_min?: number | null;
  amount_min?: number | null;
  amount_off?: number | null;
  percentage_off?: number | null;
}

interface Shipping {
  quantity_min?: number | null;
  amount_min?: number | null;
  amount_off?: number | null;
  percentage_off?: number | null;
}

interface BuyXGetY {
  quantity_min?: number | null;
  amount_min?: number | null;
  quantity_get: number;
  products_buy?: DiscountProductsList | null;
  variant_get: string | Variant;
}

interface BuyXGetYUpdateProducts {
  add: string[];
  remove: string[];
}

interface BuyXGetYUpdate {
  quantity_min?: number | null;
  amount_min?: number | null;
  quantity_get?: number | null;
  variant_get?: string | null;
  products_buy?: BuyXGetYUpdateProducts | null;
}

interface DiscountConfig {
  off_product?: OffProduct | OffProductUpdate | null;
  off_order?: OffOrder | null;
  shipping?: Shipping | null;
  buy_x_get_y?: BuyXGetY | BuyXGetYUpdate | null;
}

interface DiscountCreate extends DiscountBase {
  customers?: string[] | null;
  config: DiscountConfig;
}

interface Discount extends DiscountBase {
  id: string;
  object: typeof ObjectType.DISCOUNT;
  config: DiscountConfig;
  // TODO after adding customers to SDK
  //   customers: DiscountCustomersList;
}

interface DiscountList {
  object: string;
  url: string;
  has_more: boolean;
  data: Discount[];
}

interface DiscountUpdateCustomers {
  add?: string[] | null;
  remove?: string[] | null;
}

interface DiscountUpdate {
  active?: boolean | null;
  expires_at?: Date | null;
  applies_max?: number | null;
  customers?: DiscountUpdateCustomers | null;
  config?: DiscountConfig | null;
}

interface DiscountDelete {
  id: string;
  object: typeof ObjectType.DISCOUNT;
  deleted: boolean;
}

export type {
  Discount,
  DiscountCreate,
  DiscountUpdate,
  DiscountList,
  DiscountDelete,
};

export { DiscountTypeEnum };
