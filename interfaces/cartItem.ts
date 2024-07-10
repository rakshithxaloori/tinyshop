import { ObjectType } from "../utils/enum";

interface CartItemBase {
  quantity: number;
}

interface CartItemCreate extends CartItemBase {
  cart: string;
  price: string;
}

interface CartItem extends CartItemBase {
  id: string;
  object: typeof ObjectType.CART_ITEM;
  price: string;
}

interface CartItemList {
  object: string;
  url: string; // TODO
  has_more: boolean;
  data: CartItem[];
}

interface CartItemUpdate {
  quantity: number;
}

interface CartItemDelete {
  id: string;
  object: typeof ObjectType.CART_ITEM;
  deleted: boolean;
}

export type {
  CartItem,
  CartItemCreate,
  CartItemUpdate,
  CartItemList,
  CartItemDelete,
};
