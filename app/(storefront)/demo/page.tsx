"use server";
import Collections from "@/components/collections";
import ProductCard from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { getProductList } from "@/lib/storefront";
import BasicHeader from "@/template/header/basic";
import BasicHeroSection from "@/template/hero/basic";
import Link from "next/link";

const DemoPage = async () => {
  const headerConfig = {
    title: "Basic Header",
    dropDowns: [
      {
        title: 'Shop',

      }
    ]
  }

  const all_products_raw = await getProductList();
  const { data: all_products } = all_products_raw;
  const product_title = all_products.map((product) => {
    if (product) {
      return product.name;
    }
  });
  console.log(all_products);
  console.log(product_title.length);
  // const all_products = all_products_raw.map((product) => ({
  //   ...product,
  //   handle: product.productHandle,
  //   reviews: {
  //     rating: product.review,
  //     count: product.reviewCount
  //   }
  // }));

  return (
    <div>
      <BasicHeroSection />
      <Collections
        name="All Products"
        products={all_products}
      />
    </div>
  );
};

export default DemoPage;