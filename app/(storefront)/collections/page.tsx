import CollectionDetailsPage from "@/components/pages/collection-details-page";
import { getRootCollection } from "@/lib/storefront";
import { Metadata } from "next";
import { Suspense } from "react";

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME! as string || "tinyshop";

export const metadata: Metadata = {
  title: `Collections - ${shopName}`,
  description: "Explore all products in our collections",
};

const CollectionsPage = async () => {
  const rootCollection = await getRootCollection();

  return (
    <Suspense fallback={
      <div>Loading...</div>
    }
    >
      <CollectionDetailsPage collection={rootCollection} />
    </Suspense>
  );
}

export default CollectionsPage;