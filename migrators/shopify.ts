// Import necessary modules
import * as fs from "fs";
import * as path from "path";
import Tinyshop from "../src";
import { ProductCreate } from "../interfaces/product";
import { OptionCreate } from "../interfaces/option";
import { VariantCreate } from "../interfaces/variant";
import { PriceCreate, PriceTypeEnum } from "../interfaces/price";

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
  "https://images.unsplash.com/photo-1718615111834-c44e5bfbaca3?q=80&w=2938&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1695221087406-257eca10a2e7?q=80&w=2938&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1569541838345-b92c004f9046?q=80&w=2944&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1669749614397-2b9f87ab2168?q=80&w=2832&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
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

// Run the main function with the provided JSON file
console.log(__dirname);
// processJSONData(path.resolve(__dirname, "store_data/wellnesslanguage.json"));
processJSONData(path.resolve(__dirname, "store_data/getabranddeal.json"));
