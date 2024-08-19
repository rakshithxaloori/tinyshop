import 'server-only'
import { IProductExternalDetails, TCheckoutItem } from "@/types/product";
import { tinyshop } from "./tinyshop"
import { connectToDatabase, disconnectFromDatabase } from "./mongo";
import { daisyUIThemes } from './const';
import { CustomerUpdate } from '@tinyshop/tinyshop-node/interfaces/customer';
import { Product } from '@tinyshop/tinyshop-node/interfaces/product';
import { OptionList } from '@tinyshop/tinyshop-node/interfaces/option';
import { VariantList } from '@tinyshop/tinyshop-node/interfaces/variant';

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
    { expand: ["default_variant"] }
  );

  if (expanded_product.data.length === 0) {
    return null
  }

  const product = expanded_product.data[0];
  const { id: productId } = product;
  const [productVariants, productOptions] = await Promise.all([
    tinyshop.variants.list(productId),
    tinyshop.options.list(productId)
  ]);

  // add variants to and options to product
  let augmentedProduct: Product & { options: OptionList, variants: VariantList } = product as any;
  augmentedProduct.options = productOptions
  augmentedProduct.variants = productVariants

  console.log(augmentedProduct)

  return augmentedProduct
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
    title: "Make something people want",
    description: "",
    cta: {
      text: "Subscribe & Save 20%",
      url: "/collections/apparel",
    },
    image: {
      src: "https://ts-storefront-images.s3.ap-south-1.amazonaws.com/landing.jpeg",
      alt: "YCombinator landing page"
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

export const getProductLayoutDetails = async (brandName: string) => {
  const { client } = await connectToDatabase();
  const layoutDb = client.db('layouts');
  const storefrontLayouts = layoutDb.collection('storefront');
  // find the latest layout for the brand, the collection has createdAt field
  const layout = await storefrontLayouts.findOne({ shop: brandName });
  await disconnectFromDatabase(client);
  return layout
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
  const customer = await tinyshop.customers.verify(customerId, { otp });
  return { id: customer.id, verified: customer.is_verified }
}

export const getSubscriptionDetails = async (subscriptionId: string): Promise<TCheckoutItem[]> => {
  const subscription = await tinyshop.subscriptions.retrieve(subscriptionId);

  const itemPromises = subscription.line_items.map(async (lineItem) => {
    const { price, quantity } = lineItem;
    const { product, variant, unit_amount } = await tinyshop.prices.retrieve(price);

    const [productData, variantData] = await Promise.all([
      tinyshop.products.retrieve(product),
      tinyshop.variants.retrieve(variant)
    ]);

    const { name: productName, images } = productData;
    const { name: variantName } = variantData;

    const productImage = images ? images[0] : '';

    return {
      id: price,
      image: productImage,
      productName,
      variantName,
      quantity,
      unitAmount: unit_amount
    };
  });

  return Promise.all(itemPromises);
};

export const getCustomerAddresses = async (customerId: string) => {
  const addresses = await tinyshop.customerAddresses.list(customerId);
  return addresses
}