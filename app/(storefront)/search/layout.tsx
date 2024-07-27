import StorefrontLayout from "@/components/layout/storefront";

const SearchPageLayout = ({ children }
  : { children: React.ReactNode }
) => {
  return (
    <StorefrontLayout>
      {children}
    </StorefrontLayout>
  );
}

export default SearchPageLayout;