import { ObjectType } from "../utils/enum";

enum CartStatusEnum {
  // Define your CartStatusEnum values here
  ACTIVE = "active",
  INACTIVE = "inactive",
}

interface CartItemCreate {
  price: string;
  quantity: number;
}

interface CartBase {}

interface CartCreate extends CartBase {
  cart_item: CartItemCreate;
}

interface Cart extends CartBase {
  id: string;
  object: typeof ObjectType.CART;
  status: CartStatusEnum;
  cart_items: CartItemList;
}

interface CartList {
  object: string;
  url: string;
  has_more: boolean;
  data: Cart[];
}

interface CartUpdate {
  status?: CartStatusEnum | null;
}

interface CartDelete {
  id: string;
  object: typeof ObjectType.CART;
  deleted: boolean;
}

interface CartItemList {
  // Define the structure of CartItemList here
}

export type { Cart, CartCreate, CartUpdate, CartList, CartDelete };

export { CartStatusEnum };
