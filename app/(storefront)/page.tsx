"use server";
import CollectionDisplayList from "@/components/collection-display-list";
import ProductDisplayList from "@/components/product-display-list";
import { getCollectionList, getProductList } from "@/lib/storefront";

const StorefrontLandingPage = async () => {
  const all_products_raw = await getProductList();
  const { data: all_products } = all_products_raw;

  const all_collection_raw = await getCollectionList();
  const { data: all_collections } = all_collection_raw;

  return (
    <div className="">
      {/* <BasicHeroSection /> */}
      <ProductDisplayList
        name="All Products"
        products={all_products}
      />

      <CollectionDisplayList
        collections={all_collections}
      />


    </div>
  );
};

export default StorefrontLandingPage;