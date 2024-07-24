import ProductDetailsPage from "@/components/pages/product-details-page"
import { getAllProductHandles, getProductByHandle, getProductCollections, getProductReviews } from "@/lib/storefront";
import { Suspense } from "react";

export const experimental_ppr = true
export const dynamicParams = true

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

  return (
    <Suspense fallback={
      <div>Loading...</div>
    }>
      <ProductDetailsPage product={product} collections={collections} reviews={reviews} />
    </Suspense>
  );
}

export default ProductLandingPage;