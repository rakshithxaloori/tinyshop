import StorefrontLayout from "@/components/layout/storefront";
import { getProductDetailsPageTheme } from "@/lib/storefront";

const brandName = process.env.NEXT_PUBLIC_SHOP_NAME! as string;

const ProductDetailsPageLayout = async (
  { children, params }: {
    children: React.ReactNode;
    params: { product_handle: string };
  }
) => {
  const product_handle = decodeURIComponent(params.product_handle);
  const theme = await getProductDetailsPageTheme(brandName, product_handle);
  // console.log(theme);

  return (
    <StorefrontLayout theme={theme}>
      {children}
    </StorefrontLayout>
  );
}

export default ProductDetailsPageLayout