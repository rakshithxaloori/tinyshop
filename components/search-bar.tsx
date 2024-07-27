"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { useSearchQuery } from "./hooks/search";

const SearchBar = () => {
  const pathname = usePathname();
  const { query, setQuery, history, setHistory } = useSearchQuery();
  const router = useRouter();
  useEffect(() => {
    if (query) {
      router.push(`/search?q=${query}`)
    } else if (query !== null && history) {
      router.push(history)
    }
  }, [query, router, history])

  const handleSearchInput = (e: any) => {
    e.preventDefault();
    // search non-search pages as history
    if (pathname !== "/search") {
      setHistory(pathname)
    }
    setQuery(e.target.value);
  }

  return (
    <label className="input input-bordered flex bg-base-100 items-center gap-2 w-full">
      <input type="text" className="grow text-base-content" placeholder="Search products..."
        value={query || ""}
        onChange={handleSearchInput}
      />
      <kbd className="bg-neutral text-neutral-content kbd kbd-sm">⌘</kbd>
      <kbd className="bg-neutral text-neutral-content kbd kbd-sm">K</kbd>
    </label>
  )
}

export default SearchBar;