import StorefrontLayout from "@/components/layout/storefront";

const CheckoutPageLayout = ({ children }
  : { children: React.ReactNode }
) => {
  return (
    <StorefrontLayout>
      {children}
    </StorefrontLayout>
  );
}

export default CheckoutPageLayout;