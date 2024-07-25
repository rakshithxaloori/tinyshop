import ClientSideProvider from "../providers";
import StorefrontLayout from "@/components/layout/storefront";

const StorefrontTemplate = async (
  { children }: Readonly<{
    children: React.ReactNode;
  }>,
) => {
  return (
    <ClientSideProvider>
      <StorefrontLayout>
        {children}
      </StorefrontLayout>

    </ClientSideProvider>
  );
}

export default StorefrontTemplate;