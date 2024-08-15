import { ProductList } from "./product";

type COLLECTION_OBJECT = "collection";

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
  handle: string;
  object: COLLECTION_OBJECT;
  products: ProductList;
}

interface CollectionList {
  object: "list";
  url: "/v1/collections";
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
  object: COLLECTION_OBJECT;
  deleted: boolean;
}

export type {
  Collection,
  CollectionCreate,
  CollectionUpdate,
  CollectionList,
  CollectionDelete,
};
