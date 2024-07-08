"use client";
import PreviewNav from "@/components/preview/preview-nav";
import ClientSideProvider from "../providers";
import StorefrontLayout from "@/components/layout/storefront";

const StorefrontTemplate = (
  { children }: Readonly<{
    children: React.ReactNode;
  }>,
) => {

  return (
    <ClientSideProvider>
      <PreviewNav />
      <StorefrontLayout>
        {children}
      </StorefrontLayout>

    </ClientSideProvider>
  );
}

export default StorefrontTemplate;