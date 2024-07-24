import Api from "./api";
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

class Tinyshop {
  public customers: Customers;
  public customerAddresses: CustomerAddresses;
  public products: Products;
  public options: Options;
  public variants: Variants;
  public prices: Prices;
  public collections: Collections;
  public carts: Carts;
  public cartItems: CartItems;
  public reviews: Reviews;
  public discounts: Discounts;
  private api: Api;

  constructor(secret_key: string, base_url?: string) {
    this.api = new Api(secret_key, base_url);
    this.customers = new Customers(this.api);
    this.customerAddresses = new CustomerAddresses(this.api);
    this.products = new Products(this.api);
    this.options = new Options(this.api);
    this.variants = new Variants(this.api);
    this.prices = new Prices(this.api);
    this.collections = new Collections(this.api);
    this.carts = new Carts(this.api);
    this.cartItems = new CartItems(this.api);
    this.reviews = new Reviews(this.api);
    this.discounts = new Discounts(this.api);
  }
}

export default Tinyshop;
