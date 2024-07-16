"use client";

import SearchQueryProvider from "@/components/hooks/search";

const ClientSideProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <SearchQueryProvider>
      {children}
    </SearchQueryProvider>
  );
}

export default ClientSideProvider;