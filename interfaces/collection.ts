import { ObjectType } from "../utils/enum";
import { ProductList } from "./product";

interface CollectionBase {
  name: string;
  image_web?: string | null;
  image_mobile?: string | null;
}

interface CollectionCreate extends CollectionBase {
  products?: string[] | null;
}

interface Collection extends CollectionBase {
  id: string;
  object: typeof ObjectType.COLLECTION;
  products: ProductList;
}

interface CollectionList {
  object: string; // should be "list"
  url: string; // should be "/v1/collections"
  has_more: boolean;
  data: Collection[];
}

interface ProductsUpdate {
  add?: string[] | null;
  remove?: string[] | null;
}

interface CollectionUpdate {
  name?: string | null;
  image_web?: string | null;
  image_mobile?: string | null;
  products?: ProductsUpdate | null;
}

interface CollectionDelete {
  id: string;
  object: typeof ObjectType.COLLECTION;
  deleted: boolean;
}

export type {
  Collection,
  CollectionCreate,
  CollectionUpdate,
  CollectionList,
  CollectionDelete,
};
