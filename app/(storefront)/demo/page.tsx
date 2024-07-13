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
  console.log(all_products);

  return (
    <div className="mx-sm md:mx-2xl">
      {/* <BasicHeroSection /> */}
      <Collections
        name="All Products"
        products={all_products}
      />
    </div>
  );
};

export default DemoPage;