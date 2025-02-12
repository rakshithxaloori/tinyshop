import StorefrontLayout from "@/components/layout/storefront";

const WishlistLayout = ({ children }
  : { children: React.ReactNode }
) => {
  return (
    <StorefrontLayout>
      {children}
    </StorefrontLayout>
  );
}

export default WishlistLayout;