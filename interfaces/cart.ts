import { CartItemList } from "./cartItem";

type CART_OBJECT = "cart";

enum CartStatusEnum {
  // Define your CartStatusEnum values here
  ACTIVE = "active",
  INACTIVE = "inactive",
}

interface CartItemCreate {
  price: string;
  quantity: number;
}

interface CartBase {
  currency: string;
}

interface CartCreate extends CartBase {
  cart_item?: CartItemCreate | null;
}

interface Cart extends CartBase {
  id: string;
  object: CART_OBJECT;
  status: CartStatusEnum;
  cart_items: CartItemList;
}

interface CartList {
  object: "list";
  url: "/v1/carts";
  has_more: boolean;
  data: Cart[];
}

interface CartUpdate {
  status?: CartStatusEnum | null;
}

interface CartDelete {
  id: string;
  object: CART_OBJECT;
  deleted: boolean;
}

export type { Cart, CartCreate, CartUpdate, CartList, CartDelete };

export { CartStatusEnum };
