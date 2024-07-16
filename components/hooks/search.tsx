"use client";

import { createContext, useContext, useState } from "react";

type SearchQueryContext = {
  query: string | null;
  setQuery: (query: string | null) => void;
  clearQuery: () => void;
};

const SearchQueryContext = createContext<SearchQueryContext>({
  query: null,
  setQuery: () => { },
  clearQuery: () => { },
});

export const useSearchQuery = () => {
  const context = SearchQueryContext;

  if (!context) {
    throw new Error("useSearchQuery must be used within a <SearchQueryProvider />");
  }

  return useContext(context);
};

const SearchQueryProvider = ({ children }: { children: React.ReactNode }) => {
  const [query, setQuery] = useState<string | null>(null);

  const clearQuery = () => setQuery(null);

  return (
    <SearchQueryContext.Provider value={{ query, setQuery, clearQuery }}>
      {children}
    </SearchQueryContext.Provider>
  );
};

export default SearchQueryProvider;