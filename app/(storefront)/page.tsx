"use server";

import StorefrontLandingPage from "@/components/pages/storefront-landing-page";
import { getCollectionList, getHeroSectionDetails, getProductList } from "@/lib/storefront";
import { Suspense } from "react";

const LandingPage = async () => {
  const all_products_raw = await getProductList();
  const { data: all_products } = all_products_raw;

  const all_collection_raw = await getCollectionList();
  const { data: all_collections } = all_collection_raw;

  const heroSectionDetails = await getHeroSectionDetails();

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <StorefrontLandingPage
        heroSectionConfig={heroSectionDetails}
        products={all_products}
        collections={all_collections}
      />
    </Suspense>
  );
};

export default LandingPage;