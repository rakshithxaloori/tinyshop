import { Options } from "./option";
import { Products } from "./product";
import { Variants } from "./variant";
import { Prices } from "./price";
import { Carts } from "./cart";
import { CartItems } from "./cartItem";
import { Reviews } from "./review";
import { Discounts } from "./discount";
declare class Tinyshop {
  products: Products;
  options: Options;
  variants: Variants;
  prices: Prices;
  carts: Carts;
  cartItems: CartItems;
  reviews: Reviews;
  discounts: Discounts;
  private api;
  constructor(secret_key: string);
}
export default Tinyshop;
