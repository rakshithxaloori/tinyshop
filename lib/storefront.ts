import { tinyshop } from "./tinyshop"

export const getProductList = async () => {
  return tinyshop.products.list();
}

export const getProductByHandle = async (handle: string) => {
  return tinyshop.products.retrieve(handle);

}


