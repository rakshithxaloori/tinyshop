import { Options } from "./option";
import { Products } from "./product";
import { Variants } from "./variant";
import { Prices } from "./price";
declare class Tinyshop {
  products: Products;
  options: Options;
  variants: Variants;
  prices: Prices;
  private api;
  constructor(secret_key: string);
}
export default Tinyshop;