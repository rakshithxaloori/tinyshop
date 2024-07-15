// Import necessary modules
import * as fs from "fs";
import * as path from "path";
import Tinyshop from "../src";
import { ProductCreate } from "../interfaces/product";
import { OptionCreate } from "../interfaces/option";
import { VariantCreate } from "../interfaces/variant";
import { PriceCreate, PriceTypeEnum } from "../interfaces/price";
import Haikunator from 'haikunator'
import { FeedbackEnum } from "../interfaces/review";

const secret_key = "sk_test_1234abcd";

const tinyshop = new Tinyshop(secret_key);

// Function to read JSON data
const readJSON = (filePath: string) => {
  const data = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(data);
};

// Function to convert JSON data to ProductCreate
const convertToProductCreate = (product: any): ProductCreate => {
  return {
    name: product.title,
    description: product.body_html,
    images: product.images.map((image: any) => image.src) || [],
    active: product.status === "active",
    shippable: product.variants.some(
      (variant: any) => variant.requires_shipping
    ),
    preorder: false, // Assuming preorder information is not available
    // handle: product.handle,
  };
};

// Function to convert JSON data to OptionCreate
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

// Function to convert JSON data to VariantCreate
const convertToVariantCreate = (
  variant: any,
  productId: string
): VariantCreate => {
  return {
    name: variant.title,
    description: null, // Assuming description is not available
    active: true, // Assuming all variants are active
    options: [
      {
        name: "Default Option",
        value: variant.option1 || "Default Title",
      },
    ],
    accept_zero_inventory_orders: variant.inventory_policy === "continue",
    next_refill: new Date().toISOString(), // Placeholder for next refill date
    package_dimensions: {
      height: 0,
      width: 0,
      length: 0,
      weight: variant.weight,
    },
    product: productId,
    is_default: false,
  };
};

// Function to convert JSON data to PriceCreate
const convertToPriceCreate = (
  shVariant: any,
  tsVariantId: string
): PriceCreate => {
  return {
    active: true, // Assuming all prices are active
    currency: "INR", // Assuming currency is INR
    type: PriceTypeEnum.ONE_TIME, // TODO
    // type: "one_time",
    unit_amount: parseInt(shVariant.price),
    unit_compare_amount: shVariant.compare_at_price
      ? parseInt(shVariant.compare_at_price)
      : null,
    is_default: false,
    customer_unit_amount: {
      preset: 1,
    },
    recurring: null, // Assuming no recurring price
    variant: tsVariantId,
  };
};

const collectionImagesList = [
  "https://images.unsplash.com/photo-1523246181290-a16e4b9a00b5?q=80&w=2874&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://plus.unsplash.com/premium_photo-1682091664140-d2a290b563db?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1636581563786-accb300ddcdc?q=80&w=3002&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://plus.unsplash.com/premium_photo-1661963739183-3f701caaeabc?q=80&w=2942&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1599751449029-e4ea8f21d966?q=80&w=2256&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
]

// Main function to process JSON data
const processJSONData = async (filePath: string) => {
  const data = readJSON(filePath);
  const products = data.products;

  const activeProducts = products.filter(
    (product: any) => {
      const isActive = product.status === "active";
      const hasImage = product.images.length > 0;
      return isActive && hasImage;
    }
  );

  let shopifyIdToTinyshopProductId: any = {};

  for (const product of activeProducts) {
    const productCreate = convertToProductCreate(product);
    const product_res = await tinyshop.products.create(productCreate);
    shopifyIdToTinyshopProductId[product.id] = product_res.id;

    for (const option of product.options) {
      const optionCreate = convertToOptionCreate(option, product_res.id);
      await tinyshop.options.create(optionCreate);
    }

    for (const [index, variant] of product.variants.entries()) {
      const variantCreate = convertToVariantCreate(variant, product_res.id);
      if (index === 0) {
        variantCreate.is_default = true;
      }
      const variant_res = await tinyshop.variants.create(variantCreate);
      const priceCreate = convertToPriceCreate(variant, variant_res.id);
      await tinyshop.prices.create(priceCreate);
    }
  }

  const collections = data.custom_collections;
  console.log("Done creating products, options, variants, and prices. Now creating collections.")

  for (const collection of collections) {

    const products = collection.products.map((productId: any) => shopifyIdToTinyshopProductId[productId]);

    const collectionCreate = {
      name: collection.title,
      image_web: collectionImagesList[Math.floor(Math.random() * collectionImagesList.length)],
      image_mobile: collectionImagesList[Math.floor(Math.random() * collectionImagesList.length)],
      products: products.filter((product: any) => product !== undefined),
    };
    const collection_res = await tinyshop.collections.create(collectionCreate);
  }


  console.log("Done creating collections.");
};

function getRandomFeedbackEnum(): FeedbackEnum {
  const enumValues = Object.values(FeedbackEnum);
  const randomIndex = Math.floor(Math.random() * enumValues.length);
  return enumValues[randomIndex] as FeedbackEnum;
}

function getRandomReviewText(): string {
  const reviewList = [
    'This is a great product! I would recommend it to everyone.',
    'I am very happy with my purchase. The product is of great quality.',
    'The product was delivered on time and in good condition.',
    'I am satisfied with the product. It met my expectations.',
    'The product is as described. I am happy with my purchase.',
  ];

  const randomIndex = Math.floor(Math.random() * reviewList.length);
  return reviewList[randomIndex];
}

function getRandomPhoneNumber(): string {
  // Generate a random 10-digit number
  const randomNumber = Math.floor(1000000000 + Math.random() * 9000000000);

  // Convert the number to a string and pad it with leading zeros if necessary
  return randomNumber.toString().padStart(10, '0');
}

const createReviews = async (numCustomers: number) => {
  console.log("Creating reviews...");
  // create `numCustomers` fake customers
  const haikunator = new Haikunator();
  let customerIds: string[] = [];
  for (let i = 0; i < numCustomers; i++) {
    // create the customer
    const customerObject = {
      email: `customer${i + 1}@email.com`,
      name: haikunator.haikunate(),
      phone: getRandomPhoneNumber(),
    };

    const { id: customerId } = await tinyshop.customers.create(customerObject);
    customerIds.push(customerId);
  }


  const { data: productsData } = await tinyshop.products.list();
  for (const product of productsData) {
    // Create `numCustomers` fake reviews for each product
    for (let i = 0; i < numCustomers; i++) {
      const reviewObject = {
        product: product.id,
        customer: customerIds[i],
        product_rating: Math.floor(Math.random() * 5) + 1,
        shipping_rating: Math.floor(Math.random() * 5) + 1,
        feedback: getRandomFeedbackEnum(),
        review: getRandomReviewText(),
      };
      await tinyshop.reviews.create(reviewObject);
    }
  }
}

// Run the main function with the provided JSON file
console.log(__dirname);
// processJSONData(path.resolve(__dirname, "store_data/wellnesslanguage.json"))
processJSONData(path.resolve(__dirname, "store_data/getabranddeal.json"))
  .then(() => {
    createReviews(15);
  })