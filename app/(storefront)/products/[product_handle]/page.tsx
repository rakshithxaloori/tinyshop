import ProductCard from "@/components/product-card";
import { getProductByHandle } from "@/lib/storefront";


const ProductLandingPage = async (
  { params }: { params: { product_handle: string } },
) => {
  const product_handle = decodeURIComponent(params.product_handle);
  const raw_product = await getProductByHandle(product_handle);
  if (!raw_product) {
    return <div>Product not found</div>;
  }
  const product = {
    ...raw_product,
    handle: raw_product.handle,
  };

  return (
    <div>
      <h1>Product Landing Page</h1>
      <p>Product Handle: {product_handle}</p>
      <ProductCard product={product} />
    </div>
  );
}

export default ProductLandingPage;