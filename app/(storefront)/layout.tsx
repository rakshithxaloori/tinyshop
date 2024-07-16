import { getCartId } from "@/lib/cookie/cart";
import ClientSideProvider from "../providers";
import StorefrontLayout from "@/components/layout/storefront";

const StorefrontTemplate = async (
  { children }: Readonly<{
    children: React.ReactNode;
  }>,
) => {

  const cartId = await getCartId();

  return (
    <ClientSideProvider>
      <StorefrontLayout {...{ cartId }}>
        {children}
      </StorefrontLayout>

    </ClientSideProvider>
  );
}

export default StorefrontTemplate;