import { tinyshop } from "./tinyshop"

// "prices": {
//   "object": "list",
//   "url": "/v1/prices",
//   "has_more": false,
//   "data": [
//       {
//           "created": 1720446037,
//           "updated": 1720446037,
//           "livemode": false,
//           "active": true,
//           "currency": "INR",
//           "type": "one_time",
//           "unit_amount": 885,
//           "unit_compare_amount": null,
//           "default": false,
//           "customer_unit_amount": {
//               "maximum": null,
//               "minimum": null,
//               "preset": 1
//           },
//           "recurring": null,
//           "id": "price_T8oVetF7tNcP2sTS5ZDHuv",
//           "object": "price"
//       }
//   ]
// }
export const processPricesResponse = (prices: any) => {
  // Prices are returned as an array of objects
  // return the currency, the unit_amount and the unit_compare_amount
  // if available
  return prices.map((price: any) => {
    const { currency, unit_amount, unit_compare_amount } = price;
    return {
      currency,
      unit_amount,
      unit_compare_amount
    }
  });
}

export const getProductList = async () => {
  const all_products_raw = await tinyshop.products.list(
    {
      expand: ["default_variant"],
    }
  );
  return all_products_raw

}

export const getProductByHandle = async (handle: string) => {
  const expanded_product = await tinyshop.products.search(
    `handle:${handle}`,
    { expand: ["default_variant", "variants", "options"] }
  );

  return expanded_product
}


