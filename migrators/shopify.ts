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
    images: product.images.map((image: any) => image.src),
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
    default: false,
    customer_unit_amount: {
      preset: 1,
    },
    recurring: null, // Assuming no recurring price
    variant: tsVariantId,
  };
};

// Main function to process JSON data
const processJSONData = async (filePath: string) => {
  const data = readJSON(filePath);
  const products = data.products;

  products.forEach(async (product: any) => {
    if (product.status !== "active") return;
    const productCreate = convertToProductCreate(product);
    // productCreates.push(productCreate);
    const product_res = await tinyshop.products.create(productCreate);
    console.log(product_res);

    product.options.forEach(async (option: any) => {
      const optionCreate = convertToOptionCreate(option, product_res.id);
      // optionCreates.push(optionCreate);
      const option_res = await tinyshop.options.create(optionCreate);
      console.log(option_res);
    });

    product.variants.forEach(async (variant: any, index) => {
      const variantCreate = convertToVariantCreate(variant, product_res.id);
      if (index === 0) {
        variantCreate.is_default = true;
      }

      // variantCreates.push(variantCreate);
      const variant_res = await tinyshop.variants.create(variantCreate);
      console.log(variant_res);

      const priceCreate = convertToPriceCreate(variant, variant_res.id);
      // priceCreates.push(priceCreate);
      const price_res = await tinyshop.prices.create(priceCreate);
      console.log(price_res);
    });
  });
};

// Run the main function with the provided JSON file
console.log(__dirname);
processJSONData(path.resolve(__dirname, "store_data/wellnesslanguage.json"));
