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
import { Checkouts } from "./checkout";
import { Invoices } from "./invoice";
import { Subscriptions } from "./subscription";
import { Orders } from "./order";

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
  checkouts: Checkouts;
  invoices: Invoices;
  subscriptions: Subscriptions;
  orders: Orders;
  private api;
  constructor(secret_key: string, base_url?: string);
}
export default Tinyshop;
