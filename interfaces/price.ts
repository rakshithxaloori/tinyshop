import { ObjectType } from "../utils/enum";

// Enums for PriceTypeEnum and RecurringTypeEnum
enum PriceTypeEnum {
  ONE_TIME = "one_time",
  SUBSCRIPTION = "subscription",
}

enum RecurringTypeEnum {
  DAY = "day",
  WEEK = "week",
  MONTH = "month",
  YEAR = "year",
}

// Interface for CustomerUnitAmount
interface CustomerUnitAmount {
  maximum?: number | null;
  minimum?: number | null;
  preset: number;
}

// Interface for Recurring
interface Recurring {
  interval: RecurringTypeEnum;
  interval_count: number;
}

// Base interface for Price
interface PriceBase {
  active: boolean;
  currency: string;
  type: PriceTypeEnum;
  unit_amount: number;
  unit_compare_amount?: number | null;
  is_default: boolean;
  customer_unit_amount?: CustomerUnitAmount | null;
  recurring?: Recurring | null;
}

// Interface for PriceCreate
interface PriceCreate extends PriceBase {
  variant: string;
}

// Interface for Price
interface Price extends PriceBase {
  id: string;
  object: typeof ObjectType.PRICE;
}

// Interface for PriceList
interface PriceList {
  object: "list";
  url: "/v1/prices";
  has_more: boolean;
  data: Price[];
}

// Interface for PriceUpdate
interface PriceUpdate {
  active?: boolean | null;
  default?: boolean | null;
  unit_compare_amount?: number | null;
  customer_unit_amount?: CustomerUnitAmount | null;
  recurring?: Recurring | null;
}

// Interface for PriceDelete
interface PriceDelete {
  id: string;
  object: typeof ObjectType.PRICE;
  deleted: boolean;
}

export type { Price, PriceCreate, PriceUpdate, PriceList, PriceDelete };

export { PriceTypeEnum, RecurringTypeEnum };
