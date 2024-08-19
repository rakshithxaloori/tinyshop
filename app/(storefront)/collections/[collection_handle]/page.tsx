import CollectionDetailsPage from "@/components/pages/collection-details-page";
import { getAllCollectionHandles, getCollectionByHandle, getProductLayoutDetails } from "@/lib/storefront";
import { Metadata } from "next";
import { Suspense } from "react";

export const dynamicParams = true

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME! as string || "tinyshop";

export const generateMetadata = async ({
  params,
}: {
  params: { collection_handle: string };
}): Promise<Metadata> => {
  const collection_handle = decodeURIComponent(params.collection_handle);
  const raw_collection = await getCollectionByHandle(collection_handle);
  if (!raw_collection) {
    return {
      title: "Collection not found",
      description: "Collection not found",
    };
  }
  const collection = raw_collection.data[0];
  if (!collection) {
    return {
      title: "Collection not found",
      description: "Collection not found",
    };
  }

  const pageName = `${collection.name} - ${shopName}`;
  return {
    title: pageName,
    description: collection.name,
  };
}

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

  const mongoLayout = await getProductLayoutDetails(shopName);
  const cardLayout = mongoLayout?.layout || null;
  if (!cardLayout) {
    throw new Error('No layout found for the brand');
  }

  return (
    <Suspense fallback={
      <div>Loading...</div>
    }
    >
      <CollectionDetailsPage {...{ collection }} layout={cardLayout} />
    </Suspense>
  );
}

export default CollectionDisplayPage;