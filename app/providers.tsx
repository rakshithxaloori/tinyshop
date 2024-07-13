"use client";

import CartModalProvider from "@/components/hooks/cart";
// import { PreviewProvider } from "@/components/preview/context";

const ClientSideProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    // <PreviewProvider>
    <CartModalProvider>
      {children}
    </CartModalProvider>
    // </PreviewProvider>
  );
}

export default ClientSideProvider;