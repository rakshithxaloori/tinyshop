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

export const getRootCollection = async () => {
  const rootCollectionImage = "https://images.unsplash.com/photo-1496449903678-68ddcb189a24?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
  const name = "All Products";

  const all_products_raw = await getProductList();
  const rootCollection = {
    name,
    image_web: rootCollectionImage,
    products: all_products_raw
  }
  return rootCollection
}

export const getProductList = async () => {
  const all_products_raw = await tinyshop.products.list(
    {
      expand: ["default_variant"],
    }
  );
  return all_products_raw

}

export const getCollectionList = async () => {
  const collections = await tinyshop.collections.list();
  return collections
}

export const getCollectionByHandle = async (handle: string) => {
  const collection = await tinyshop.collections.search(`handle:${handle}`,
    { expand: ["products"] }
  );
  return collection
}

export const getHeaderNavItems = async () => {
  const collections_raw = await getCollectionList();
  const { data: collections } = collections_raw;
  const navItems = collections.map((collection: any) => {
    return {
      name: collection.name,
      url: `/collections/${collection.handle}`,
      description: 'All products in this collection'
    }
  });

  return navItems;
}

export const getProductByHandle = async (handle: string) => {
  const expanded_product = await tinyshop.products.search(
    `handle:${handle}`,
    { expand: ["default_variant", "variants", "options"] }
  );

  return expanded_product
}

export const getHeroSectionDetails = async () => {
  const heroSectionDetails = {
    title: "Discover the best products",
    description: "We have a wide range of products to suit your needs. Check them out now!",
    cta: {
      text: "Shop Now",
      url: "/collections",
    },
    image: {
      src: "https://images.unsplash.com/photo-1496449903678-68ddcb189a24?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      alt: "Hero Section Image"
    }
  }
  return heroSectionDetails
}

export const getProductCollections = async (product: any) => {
  const { id: productId } = product;
  const collectionsRaw = await getCollectionList();
  const { data: collections } = collectionsRaw;
  let productCollections = [];
  for (let collection of collections) {
    const { products: productsRaw } = collection;
    const { data: products } = productsRaw;
    for (let colProdId of products) {
      if (colProdId === productId) {
        productCollections.push(
          {
            name: collection.name,
            url: `/collections/${collection.handle}`
          }
        )
      }
    }
  }


  return productCollections
}