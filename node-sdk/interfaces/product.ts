import { Variant } from "./variant";

type PRODUCT_OBJECT = "product";

interface ProductBase {
  name: string;
  description?: string;
  images?: string[];
  active: boolean;
  shippable: boolean;
  preorder: boolean;
}

interface ProductCreate extends ProductBase {}

interface Product extends ProductBase {
  id: string;
  handle: string;
  object: PRODUCT_OBJECT;
  default_variant?: Variant | null;
  rating?: number | null;
}

interface ProductList {
  object: "list";
  url: "/v1/products";
  has_more: boolean;
  data: Product[];
}

interface ProductUpdate {
  name?: string;
  description?: string;
  active?: boolean;
  shippable?: boolean;
  preorder?: boolean;
}

interface ProductDelete {
  id: string;
  object: PRODUCT_OBJECT;
  deleted: boolean;
}

export type {
  Product,
  ProductCreate,
  ProductUpdate,
  ProductList,
  ProductDelete,
};
