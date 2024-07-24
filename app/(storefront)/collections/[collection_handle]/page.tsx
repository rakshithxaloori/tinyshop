import CollectionDetailsPage from "@/components/pages/collection-details-page";
import { getAllCollectionHandles, getCollectionByHandle } from "@/lib/storefront";
import { Suspense } from "react";

export const experimental_ppr = true
export const dynamicParams = true

export const generateStaticParams = async () => {
  const collectionHandles = await getAllCollectionHandles();
  const staticPaths = collectionHandles.map((handle) => ({
    collection_handle: handle
  }));
  return staticPaths;
}

const CollectionDisplayPage = async (
  { params }: { params: { collection_handle: string } },
) => {
  const collection_handle = decodeURIComponent(params.collection_handle);
  const raw_collection = await getCollectionByHandle(collection_handle);
  if (!raw_collection) {
    return <div>Collection not found</div>;
  }
  const {
    data: collection_list,
  } = raw_collection;

  if (collection_list.length === 0) {
    return <div>Collection not found</div>;
  }

  const collection = collection_list[0];


  return (
    <Suspense fallback={
      <div>Loading...</div>
    }
    >
      <CollectionDetailsPage {...{ collection }} />
    </Suspense>
  );
}

export default CollectionDisplayPage;