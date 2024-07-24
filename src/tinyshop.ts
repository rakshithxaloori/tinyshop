import Api from "./api";
import { Options } from "./option";
import { Products } from "./product";
import { Variants } from "./variant";
import { Prices } from "./price";

class Tinyshop {
  public products: Products;
  public options: Options;
  public variants: Variants;
  public prices: Prices;
  private api: Api;

  constructor(secret_key: string, base_url?: string) {
    this.api = new Api(secret_key, base_url);
    this.products = new Products(this.api);
    this.options = new Options(this.api);
    this.variants = new Variants(this.api);
    this.prices = new Prices(this.api);
  }
}

export default Tinyshop;