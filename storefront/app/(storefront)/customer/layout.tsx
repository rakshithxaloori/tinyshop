
import StorefrontLayout from "@/components/layout/storefront";

const StorefrontTemplate = async (
  { children }: Readonly<{
    children: React.ReactNode;
  }>,
) => {
  return (
    <StorefrontLayout>
      {children}
    </StorefrontLayout>
  );
}

export default StorefrontTemplate;