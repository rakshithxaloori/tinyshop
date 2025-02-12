import StorefrontLayout from "@/components/layout/storefront";

const CheckoutLayout = async (
  { children }: {
    children: React.ReactNode;
  }
) => {
  return (
    <StorefrontLayout>
      {children}
    </StorefrontLayout>
  );
}

export default CheckoutLayout