import { ObjectType } from "../utils/enum";

// Interface for VariantOptionValue
interface VariantOptionValue {
  name: string;
  value: string;
}

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
  options?: VariantOptionValue[] | null;
  accept_zero_inventory_orders: boolean;
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
  object: typeof ObjectType.VARIANT;
}

// Interface for VariantList
interface VariantList {
  object: "list";
  url: string;
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
  options?: VariantOptionValue[] | null;
  accept_zero_inventory_orders?: boolean | null;
  next_refill?: string | null; // Using string to represent datetime in ISO format
  package_dimensions?: PackageDimensionsUpdate | null;
}

// Interface for VariantDelete
interface VariantDelete {
  id: string;
  object: typeof ObjectType.VARIANT;
  deleted: boolean;
}

export type {
  Variant,
  VariantCreate,
  VariantUpdate,
  VariantList,
  VariantDelete,
};
