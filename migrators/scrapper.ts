// Migrator for the custom scrapper shopify data
import dotenv from "dotenv";
dotenv.config();

import * as fs from "fs";
import * as path from "path";
import Tinyshop from "../src";
import { Product, ProductCreate } from "../interfaces/product";
import { OptionCreate } from "../interfaces/option";
import { VariantCreate } from "../interfaces/variant";
import {
  PriceCreate,
  PriceTypeEnum,
  RecurringTypeEnum,
} from "../interfaces/price";
import { CollectionCreate } from "../interfaces/collection";
import { CustomerCreate } from "../interfaces/customer";
import { FeedbackEnum, ReviewCreate } from "../interfaces/review";
import { MongoClient, Collection } from "mongodb";

import algoliasearch, { SearchClient, SearchIndex } from 'algoliasearch';


const secret_key = process.env.SECRET_KEY as string;
const apiHost = process.env.API_HOST as string;
const tinyshop = new Tinyshop(secret_key, apiHost);

type TScrapperVariant = {
  extId: number;
  name: string;
  price: number;
  compareAtPrice: number;
  available: boolean;
};

type TScrapperProduct = {
  url: string;
  name: string;
  extId: number;
  description: string;
  faq: {
    question: string;
    answer: string;
  }[];
  images: {
    src: string;
    alt: string;
  }[];
  reviews: {
    name: string;
    date: string;
    score: number;
    title: string;
    text: string;
  }[];
  variants: TScrapperVariant[];
  options: {
    name: string;
    values: string[];
  }[];
  tabs: {
    data: {
      title: string;
      content: {
        text: string;
        image: {
          src: string;
          alt: string;
        };
      };
    };
  }[];
};

type TScrapperProductData = TScrapperProduct[];

type TScrapperCollection = {
  length: number;
  url: string;
  extId: string; // there is a mismatch of extId in the collection and product data. fix it in the scrapper
  name: string;
  data: {
    product_id: string;
    product_title: string;
    default_variant_name: string; // NO-USE
    product_image: string;
  }[];
};

type TScrapperCollectionData = TScrapperCollection[];

type TScrapperCollectionJson = {
  brand: string;
  data: TScrapperCollectionData;
};

// MongoDB connection string from environment variables
const MONGO_URI = process.env.MONGO_URI as string;
const DB_NAME = process.env.DB_NAME as string;
const COLLECTION_NAME = process.env.COLLECTION_NAME as string;

let mongoClient: MongoClient;
let productDetailsCollection: Collection;

// Function to connect to MongoDB
async function connectToMongoDB() {
  try {
    mongoClient = new MongoClient(MONGO_URI);
    await mongoClient.connect();
    console.log("Connected to MongoDB");
    const db = mongoClient.db(DB_NAME);
    productDetailsCollection = db.collection(COLLECTION_NAME);

    // Create indexes
    await productDetailsCollection.createIndex({ brand: 1 });
    await productDetailsCollection.createIndex({ product_handle: 1 });
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
    throw error;
  }
}

// Function to close MongoDB connection
async function closeMongoDBConnection() {
  if (mongoClient) {
    await mongoClient.close();
    console.log("Closed MongoDB connection");
  }
}

// Function to read JSON data
const readJSON = (filePath: string) => {
  const data = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(data);
};

// Function to convert TScrapperProduct to ProductCreate
const convertToProductCreate = (product: TScrapperProduct): ProductCreate => {
  return {
    name: product.name,
    description: product.description,
    images: product.images.map((image) => image.src).slice(0, 7) || [],
    active: true,
    shippable: product.variants.some((variant) => variant.available),
    preorder: false,
  };
};

// Function to convert TScrapperProduct to OptionCreate
const convertToOptionCreate = (
  option: any,
  productId: string
): OptionCreate => {
  return {
    name: option.name,
    values: option.values,
    product: productId,
  };
};

// Function to convert TScrapperProduct to VariantCreate
const convertToVariantCreate = (
  variant: TScrapperVariant,
  productId: string
): VariantCreate => {
  return {
    name: variant.name,
    description: null,
    active: variant.available,
    options: JSON.stringify([
      {
        name: variant.name,
        value: variant.name,
      },
    ]),
    accept_zero_inventory_orders: true,
    next_refill: Math.floor(Date.now() / 1000),
    package_dimensions: {
      height: 0,
      width: 0,
      length: 0,
      weight: 0,
    },
    product: productId,
    is_default: false,
  };
};

// Function to convert TScrapperProduct to PriceCreate
const convertToPriceCreate = (
  variant: TScrapperVariant,
  tinyshopVariantId: string
): PriceCreate => {
  const price = Math.floor(variant.price);
  const compareAtPrice = Math.floor(variant.compareAtPrice);
  return {
    active: variant.available,
    currency: "INR",
    type: PriceTypeEnum.ONE_TIME,
    unit_amount: price,
    unit_compare_amount: compareAtPrice > price ? compareAtPrice : null,
    is_default: false,
    customer_unit_amount: {
      preset: 1,
    },
    recurring: null,
    variant: tinyshopVariantId,
  };
};

const convertToRecurringPriceCreate = (
  variant: TScrapperVariant,
  tinyshopVariantId: string
): PriceCreate => {
  const price = Math.floor(variant.price * 0.8);
  const compareAtPrice = Math.floor(variant.compareAtPrice);
  return {
    active: variant.available,
    currency: "INR",
    type: PriceTypeEnum.RECURRING,
    unit_amount: price,
    unit_compare_amount: null,
    is_default: false,
    customer_unit_amount: {
      preset: 1,
    },
    recurring: {
      interval: RecurringTypeEnum.MONTH,
      interval_count: 1,
    },
    variant: tinyshopVariantId,
  };
};

// Function to convert TScrapperCollection to CollectionCreate
const convertToCollectionCreate = (
  collection: TScrapperCollection,
  tinyshopProducts: string[]
): CollectionCreate => {
  return {
    name: collection.name,
    image_web: collection.data[0].product_image,
    image_mobile: collection.data[0].product_image,
    products: tinyshopProducts,
  };
};

function getRandomFeedbackEnum(): FeedbackEnum {
  const enumValues = Object.values(FeedbackEnum);
  const randomIndex = Math.floor(Math.random() * enumValues.length);
  return enumValues[randomIndex] as FeedbackEnum;
}

// TODO: upload to product data JSON to mongoDB
async function uploadProductDetailsToMongoDB(
  tinyshopProduct: Product,
  scrapperProduct: TScrapperProduct,
  brand: string
) {
  const productHandle = tinyshopProduct.handle;
  const productDetails = {
    brand,
    product_handle: productHandle,
    faq: scrapperProduct.faq,
    tabs: scrapperProduct.tabs,
  };

  try {
    await productDetailsCollection.updateOne(
      { brand, product_handle: productHandle },
      { $set: productDetails },
      { upsert: true }
    );
    console.log(`Uploaded details for product: ${tinyshopProduct.name}`);
  } catch (error) {
    console.error(
      `Error uploading details for product ${tinyshopProduct.name}:`,
      error
    );
  }
}

function getHandle(name: string): string {
  // Normalize the product name to NFKD form
  let handle: string = name.normalize("NFKD");
  // Convert to lowercase
  handle = handle.toLowerCase();
  // Replace spaces and special characters with hyphens
  handle = handle.replace(/\s+/g, "-");
  // Remove non-alphanumeric characters except for hyphens
  handle = handle.replace(/[^a-z0-9-]/g, "");
  // Remove leading and trailing hyphens
  handle = handle.replace(/^-+|-+$/g, "");
  return handle;
}

const processCombinedJSON = async (
  productFilePath: string,
  collectionFilePath: string
) => {
  const productData: TScrapperProductData = readJSON(productFilePath);
  const { brand, data: collectionData }: TScrapperCollectionJson =
    readJSON(collectionFilePath);

  await connectToMongoDB();

  const activeProducts = productData;
  const numProducts = activeProducts.length;
  // this is a map of product's extId -> tinyshop product id
  let shopifyIdToTinyshopProductId: any = {};

  // Add products, options, variants, prices and reviews
  let phNumberRangeCount = 999997999;
  let emailRangeCount = 2000;
  let lastProgressProduct = 0;
  for (const [index, product] of activeProducts.entries()) {
    const progress = Math.floor(((index + 1) / numProducts) * 100);
    if (progress !== lastProgressProduct) {
      lastProgressProduct = progress;
    }

    const { name, variants } = product;
    if (variants.length === 0) {
      console.log(
        `Skipping product with no variants ${index + 1
        }/${numProducts} (${progress}%)`
      );
      continue;
    }

    let uniqueProductNames: string[] = [];

    console.log(`Creating product ${index + 1}/${numProducts} (${progress}%)`);
    const productCreate = convertToProductCreate(product);
    const productHandle = getHandle(productCreate.name);

    const existingProduct = uniqueProductNames.find(
      (ph) => ph == productHandle
    );
    console.log(`Product handle: ${productHandle}`, existingProduct);
    if (existingProduct) {
      console.log(
        `Product with name ${productCreate.name} already exists. Skipping.`
      );
      continue;
    }
    uniqueProductNames.push(productHandle);

    const createdProduct = await tinyshop.products.create(productCreate);
    shopifyIdToTinyshopProductId[product.extId] = createdProduct.id;

    // upload to mongoDB
    await uploadProductDetailsToMongoDB(createdProduct, product, brand);

    // maintain a set for unique options
    const optionSet = new Set<string>();
    for (const option of product.options) {
      if (optionSet.has(option.name)) {
        continue;
      }
      optionSet.add(option.name);
      const optionCreate = convertToOptionCreate(option, createdProduct.id);
      await tinyshop.options.create(optionCreate);
    }

    for (const [index, variant] of product.variants.entries()) {
      const variantCreate = convertToVariantCreate(variant, createdProduct.id);
      if (index === 0) {
        // make the first variant the default
        variantCreate.is_default = true;
      }
      const createdVariant = await tinyshop.variants.create(variantCreate);

      const priceCreate = convertToPriceCreate(variant, createdVariant.id);

      const priceCreated = await tinyshop.prices.create(priceCreate);

      const recurringPriceCreate = convertToRecurringPriceCreate(
        variant,
        createdVariant.id
      );
      await tinyshop.prices.create(recurringPriceCreate);
    }

    // Add reviews. Insert atmost 20 reviews for each product
    const reviewsSlice = product.reviews.slice(0, 20);
    for (const review of reviewsSlice) {
      // create a new customer for each review
      const customerCreate: CustomerCreate = {
        name: review.name,
        email: `customer${emailRangeCount}@email.com`,
        phone: phNumberRangeCount.toString().padStart(10, "0"),
        send_otp: true,
      };
      emailRangeCount++;
      phNumberRangeCount--;

      const { id: customerId } = await tinyshop.customers.create(
        customerCreate
      );

      const _ = await tinyshop.customers.verify(customerId, {
        otp: "000000",
      });

      const reviewCreate: ReviewCreate = {
        product: createdProduct.id,
        customer: customerId,
        product_rating: review.score,
        shipping_rating: review.score,
        feedback: getRandomFeedbackEnum(),
        review: review.text,
      };
      await tinyshop.reviews.create(reviewCreate);
    }
  }

  console.log(
    "Done creating products, options, variants, prices and reviews. Now creating collections."
  );

  // Add collections

  let lastProgressCollection = 0;
  for (const [index, collection] of collectionData.entries()) {
    const progress = Math.floor(((index + 1) / collectionData.length) * 100);
    if (progress !== lastProgressCollection) {
      lastProgressCollection = progress;
    }

    if (collection.length === 0) {
      console.log(
        `Skipping empty collection ${index + 1}/${collectionData.length
        } (${progress}%)`
      );
      continue;
    }

    const products = collection.data
      .map((product) => shopifyIdToTinyshopProductId[product.product_id])
      .filter((product) => product !== undefined);
    if (products.length === 0) {
      console.log(
        `Skipping collection with no products ${index + 1}/${collectionData.length
        } (${progress}%)`
      );
      continue;
    }

    console.log(
      `Creating collection ${index + 1}/${collectionData.length} (${progress}%)`
    );

    const collectionCreate = convertToCollectionCreate(
      collection,
      products.filter((product: any) => product !== undefined)
    );
    const collection_res = await tinyshop.collections.create(collectionCreate);
  }
  console.log("Done creating collections.");

  // Close MongoDB connection
  await closeMongoDBConnection();
};

async function main() {
  const productFilePath = path.join(
    __dirname,
    "store_data/yc_products.json"
  );
  const collectionFilePath = path.join(
    __dirname,
    "store_data/yc_collections.json"
  );

  await processCombinedJSON(productFilePath, collectionFilePath);

  // Post migration
  await postMigration();
}

const cleanDescription = (description: string): string => {
  return description.replace(/<[^>]*>?/gm, '');
}

const processProduct = (product: any): any => {
  return {
    id: product.id,
    description: product.description ? cleanDescription(product.description) : "",
    handle: product.handle,
    name: product.name,
    images: product.images || [],
    default_variant: {
      name: product.default_variant.name,
      id: product.default_variant.id,
      prices: {
        data: product.default_variant.prices.data.map((price: any) => {
          return {
            type: price.type,
            id: price.id,
            currency: price.currency,
            unit_amount: price.unit_amount,
            unit_compare_amount: price.unit_compare_amount,
          };
        }),
      },
    },
  };
}

const configureAlgoliaIndex = async (index: SearchIndex, settings: any) => {
  const algoliaSettings = {
    searchableAttributes: settings.searchableAttributes || [],
    attributesForFaceting: [
      ...settings.filterableAttributes.map((attr: string) => `filterOnly(${attr})`) || [],
      ...settings.facets || [],
    ],
  };
  const resp = await index.setSettings(algoliaSettings);
  return resp;
}

const postMigration = async () => {
  const productList = await tinyshop.products.list({ expand: ["default_variant"], });
  const algoliaRecordList = productList.data.map((product: any) => {
    const productRecord = processProduct(product);
    return {
      shopId: process.env.SHOP_ID,
      ...productRecord
    };
  }
  );

  const appId = process.env.ALGOLIA_APP_ID as string;
  const apiKey = process.env.ALGOLIA_API_KEY as string;
  const indexName = process.env.ALGOLIA_INDEX_NAME as string;

  const client = algoliasearch(appId, apiKey);
  const index = client.initIndex(indexName);

  // check if index exists
  const indexExists = await client.listIndices().then((resp) => {
    return resp.items.some((item) => item.name === indexName);
  });
  // if index exists, delete all the products matching the shopId
  if (indexExists) {
    const query = `shopId:${process.env.SHOP_ID}`;
    const deleteResp = await index.deleteBy({
      filters: query,
    });
    console.log(deleteResp);
  }

  const resp = await index.saveObjects(algoliaRecordList, {
    autoGenerateObjectIDIfNotExist: true
  });
  const settings = {
    searchableAttributes: ["name", "description"],
    filterableAttributes: ["shopId"],
  };
  const configureResp = await configureAlgoliaIndex(index, settings);
  console.log(configureResp);

  console.log("Post migration completed successfully");
}

main()
  .then(() => {
    console.log("Migration completed successfully");
  })
  .catch((error) => {
    console.error("Migration failed with error:", error);
  })
  .finally(async () => {
    await closeMongoDBConnection();
    process.exit(0);
  });
