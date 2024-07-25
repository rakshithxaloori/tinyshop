import ProductDetailsPage from "@/components/pages/product-details-page"
import { getAllProductHandles, getProductByHandle, getProductCollections, getProductExternalDetails, getProductReviews } from "@/lib/storefront";
import { Suspense } from "react";
import Loading from "./loading";

export const experimental_ppr = true
export const dynamicParams = true

const brandName = process.env.NEXT_PUBLIC_SHOP_NAME! as string;

export const generateStaticParams = async () => {
  const productHandles = await getAllProductHandles();
  const staticPaths = productHandles.map((handle) => ({
    product_handle: handle
  })
  );
  return staticPaths;
}

const ProductLandingPage = async (
  { params }: { params: { product_handle: string } },
) => {
  const product_handle = decodeURIComponent(params.product_handle);
  const raw_product = await getProductByHandle(product_handle);
  if (!raw_product) {
    return <div>Product not found</div>;
  }
  const product = raw_product.data[0];
  const collections = await getProductCollections(product);

  const reviews = await getProductReviews(product);

  const externalDetails = await getProductExternalDetails(brandName, product_handle);

  return (
    <Suspense fallback={
      <Loading />
    }>
      <ProductDetailsPage
        product={product}
        collections={collections}
        reviews={reviews}
        faqs={externalDetails?.faq || null}
        tabs={externalDetails?.tabs?.data || []}
      />
    </Suspense>
  );
}

export default ProductLandingPage;