import StorefrontLayout from "@/components/layout/storefront";

const CollectionPageLayout = ({ children }
  : { children: React.ReactNode }
) => {
  return (
    <StorefrontLayout>
      {children}
    </StorefrontLayout>
  );
}

export default CollectionPageLayout;