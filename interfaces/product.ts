import { ObjectType } from "../utils/enum";

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
  object: typeof ObjectType.PRODUCT;
}

interface ProductList {
  object: "list";
  url: "/v1/products";
  has_more: boolean;
  data: Product[];
}

interface ProductUpdate {
  name?: string;
  handle?: string;
  description?: string;
  active?: boolean;
  shippable?: boolean;
  preorder?: boolean;
}

interface ProductDelete {
  id: string;
  object: typeof ObjectType.PRODUCT;
  deleted: boolean;
}

export type {
  Product,
  ProductCreate,
  ProductUpdate,
  ProductList,
  ProductDelete,
};
