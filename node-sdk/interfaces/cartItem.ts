type CART_ITEM_OBJECT = "cart_item";

interface CartItemBase {
  quantity: number;
}

interface CartItemCreate extends CartItemBase {
  cart: string;
  price: string;
}

interface CartItem extends CartItemBase {
  id: string;
  object: CART_ITEM_OBJECT;
  price: string;
}

interface CartItemList {
  object: "list";
  url: string; // TODO
  has_more: boolean;
  data: CartItem[];
}

interface CartItemUpdate {
  quantity: number;
}

interface CartItemDelete {
  id: string;
  object: CART_ITEM_OBJECT;
  deleted: boolean;
}

export type {
  CartItem,
  CartItemCreate,
  CartItemUpdate,
  CartItemList,
  CartItemDelete,
};
