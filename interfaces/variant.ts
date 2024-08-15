import { PriceList } from "./price";

type VARIANT_OBJECT = "variant";

// Interface for VariantOptionValue
// interface VariantOptionValue {
//   name: string;
//   value: string;
// }

// Interface for PackageDimensions
interface PackageDimensions {
  height: number;
  width: number;
  length: number;
  weight: number;
}

// Base interface for Variant
interface VariantBase {
  name: string;
  description?: string | null;
  active: boolean;
  options?: string | null;
  accept_zero_inventory_orders: boolean;
  image?: string | null;
  next_refill: number; // Timestamp
  package_dimensions?: PackageDimensions | null;
  is_default: boolean;
}

// Interface for VariantCreate
interface VariantCreate extends VariantBase {
  product: string;
}

// Interface for Variant
interface Variant extends VariantBase {
  id: string;
  object: VARIANT_OBJECT;
  prices?: PriceList | null;
}

// Interface for VariantList
interface VariantList {
  object: "list";
  url: "/v1/variants";
  has_more: boolean;
  data: Variant[];
}

// Interface for PackageDimensionsUpdate
interface PackageDimensionsUpdate {
  height?: number | null;
  width?: number | null;
  length?: number | null;
  weight?: number | null;
}

// Interface for VariantUpdate
interface VariantUpdate {
  name?: string | null;
  description?: string | null;
  active?: boolean | null;
  options?: string | null;
  accept_zero_inventory_orders?: boolean | null;
  image?: string | null;
  next_refill?: number | null; // Timestamp
  package_dimensions?: PackageDimensionsUpdate | null;
  is_default?: boolean | null;
}

// Interface for VariantDelete
interface VariantDelete {
  id: string;
  object: VARIANT_OBJECT;
  deleted: boolean;
}

export type {
  Variant,
  VariantCreate,
  VariantUpdate,
  VariantList,
  VariantDelete,
};
