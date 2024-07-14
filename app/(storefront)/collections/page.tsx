import CollectionDetailsPage from "@/components/pages/collection-details-page";
import { getRootCollection } from "@/lib/storefront";
import { Suspense } from "react";

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