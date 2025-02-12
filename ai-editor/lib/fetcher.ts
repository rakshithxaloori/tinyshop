import { tinyshop } from "./tinyshop";

export const getProductList = async () => {
  const all_products_raw = await tinyshop.products.list(
    {
      expand: ["default_variant"],
    }
  );
  return all_products_raw
}