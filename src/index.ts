import Api from "./api";
import { Options } from "./option";
import { Products } from "./product";
import { Variants } from "./variant";
import { Prices } from "./price";
import { Carts } from "./cart";
import { CartItems } from "./cartItem";
import { Reviews } from "./review";
import { Discounts } from "./discount";

class Tinyshop {
  public products: Products;
  public options: Options;
  public variants: Variants;
  public prices: Prices;
  public carts: Carts;
  public cartItems: CartItems;
  public reviews: Reviews;
  public discounts: Discounts;
  private api: Api;

  constructor(secret_key: string) {
    this.api = new Api(secret_key);
    this.products = new Products(this.api);
    this.options = new Options(this.api);
    this.variants = new Variants(this.api);
    this.prices = new Prices(this.api);
    this.carts = new Carts(this.api);
    this.cartItems = new CartItems(this.api);
    this.reviews = new Reviews(this.api);
    this.discounts = new Discounts(this.api);
  }
}

export default Tinyshop;
