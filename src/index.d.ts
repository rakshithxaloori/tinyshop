import { Customers } from "./customer";
import { CustomerAddresses } from "./customerAddress";
import { Options } from "./option";
import { Products } from "./product";
import { Variants } from "./variant";
import { Prices } from "./price";
import { Collections } from "./collection";
import { Carts } from "./cart";
import { CartItems } from "./cartItem";
import { Reviews } from "./review";
import { Discounts } from "./discount";

declare class Tinyshop {
  customers: Customers;
  customerAddresses: CustomerAddresses;
  products: Products;
  options: Options;
  variants: Variants;
  prices: Prices;
  collections: Collections;
  carts: Carts;
  cartItems: CartItems;
  reviews: Reviews;
  discounts: Discounts;
  private api;
  constructor(secret_key: string);
}
export default Tinyshop;
