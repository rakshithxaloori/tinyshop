"use client";

import { PreviewProvider } from "@/components/preview/context";

const ClientSideProvider = ({ children }: { children: React.ReactNode }) => {
  return <PreviewProvider>
    {children}
  </PreviewProvider>;
}

export default ClientSideProvider;