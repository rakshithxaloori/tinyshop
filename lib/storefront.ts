import 'server-only'
import { IProductExternalDetails } from "@/types/product";
import { tinyshop } from "./tinyshop"
import { connectToDatabase, disconnectFromDatabase } from "./mongo";
import { daisyUIThemes } from './const';
import { CustomerUpdate } from '@tinyshop/tinyshop-node/interfaces/customer';

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

export const getAllProductHandles = async () => {
  const all_products_raw = await getProductList();
  const { data: all_products } = all_products_raw;
  const productHandles = all_products.map((product: any) => product.handle);
  return productHandles
}

export const getCollectionList = async () => {
  const collections = await tinyshop.collections.list();
  return collections
}

export const getAllCollectionHandles = async () => {
  const collections = await getCollectionList();
  const { data: all_collections } = collections;
  const collectionHandles = all_collections.map((collection: any) => collection.handle);
  return collectionHandles
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
  }).slice(0, 4);
  // slice navItems to 4 items

  return navItems;
}

export const getProductByHandle = async (handle: string) => {
  const expanded_product = await tinyshop.products.search(
    `handle:${handle}`,
    { expand: ["default_variant", "variants", "options"] }
  );

  return expanded_product
}

export const getWishlistProductDetails = async (productIdList: string[]) => {
  const wishlistProductDetails = [];
  for (let productId of productIdList) {
    const product = await tinyshop.products.retrieve(productId,
      { expand: ["default_variant"] }
    );
    wishlistProductDetails.push(product);
  }
  return wishlistProductDetails
}

export const getHeroSectionDetails = async () => {
  const heroSectionDetails = {
    title: "Gut Loving. Functional. Monsoon favourites.",
    description: "",
    cta: {
      text: "Subscribe & Save 20%",
      url: "/collections/digestion",
    },
    image: {
      src: "https://cosmix.in/cdn/shop/files/Gut_BFF_de4f04aa-5c0b-4bb6-83f1-ed155b95aefb.jpg",
      alt: "Gut BFF Product Image"
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

export const getProductReviews = async (product: any) => {
  const { id: productId } = product;
  const { data: reviews } = await tinyshop.reviews.list(productId);
  return reviews
}

export const getProductExternalDetails = async (brandName: string, productHandle: string): Promise<IProductExternalDetails | null> => {
  const { client, db } = await connectToDatabase();
  const collectionName = process.env.MONGO_COLLECTION_NAME as string;
  const collection = db.collection(collectionName);

  const productDetails = await collection.findOne({ brand: brandName, product_handle: productHandle }) as IProductExternalDetails | null;
  // TODO: figure out a way to create pool of clients
  await disconnectFromDatabase(client);
  return productDetails;
}

export const getProductDetailsPageTheme = async (brandName: string, productHandle: string): Promise<string> => {
  const theme = daisyUIThemes[Math.floor(Math.random() * daisyUIThemes.length)];
  return theme
}


export const getAllProductImages = async () => {
  const all_products_raw = await getProductList();
  const { data: all_products } = all_products_raw;
  const productImages = all_products.map((product: any) => {
    const { images } = product;
    if (images.length) {
      return images[0]
    }
  });

  return productImages
}

export const createOrGetCustomer = async (phoneNumber: string) => {
  const { id, is_verified: verified } = await tinyshop.customers.create({ phone: phoneNumber, send_otp: true });
  return { id, verified }
}

export const verifyCustomer = async (customerId: string, otp: string) => {
  const customer = await tinyshop.customers.update(customerId, { otp });
  return { id: customer.id, verified: customer.is_verified }
}
