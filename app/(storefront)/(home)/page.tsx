import StorefrontLandingPage from "@/components/pages/storefront-landing-page";
import { getAllProductImages, getCollectionList, getHeroSectionDetails, getProductLayoutDetails, getProductList } from "@/lib/storefront";
import { Metadata } from "next";
import { Suspense } from "react";

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME! as string || "tinyshop";
export const metadata: Metadata = {
  title: `Home - ${shopName}`,
  description: `Welcome to ${shopName}`,
};

const LandingPage = async () => {
  const all_products_raw = await getProductList();
  const { data: all_products } = all_products_raw;

  const all_collection_raw = await getCollectionList();
  const { data: all_collections } = all_collection_raw;

  // show two collections
  const featuredCollection = [
    'no-nonsense-plant-protein',
    'functional-foods'
  ]

  const featuredCollections = all_collections.filter((collection: any) => featuredCollection.includes(collection.handle));

  const heroSectionDetails = await getHeroSectionDetails();

  const carouselImages = await getAllProductImages();

  const mongoLayout = await getProductLayoutDetails(shopName);
  const cardLayout = mongoLayout?.layout || null;
  if (!cardLayout) {
    throw new Error('No layout found for the brand');
  }

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <StorefrontLandingPage
        heroSectionConfig={heroSectionDetails}
        products={all_products}
        collections={featuredCollections}
        carouselImages={carouselImages}
        productCardLayout={cardLayout}
      />
    </Suspense>
  );
};

export default LandingPage;