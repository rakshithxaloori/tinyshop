"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef } from "react";
import { useSearchQuery } from "./hooks/search";
import { SearchIcon } from "lucide-react"

const SearchBar = () => {
  const pathname = usePathname();
  const { query, setQuery, history, setHistory } = useSearchQuery();
  const router = useRouter();
  const ref = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (query) {
      router.push(`/search?q=${query}`)
    } else if (query !== null && history) {
      router.push(history)
    }
  }, [query, router, history])

  useEffect(() => {
    if (ref.current && query?.length) {
      ref.current.focus();
    }
  }, [query])

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
        ref={ref}
        value={query || ""}
        onChange={handleSearchInput}
      />
      <SearchIcon />
      <kbd className="bg-neutral text-neutral-content kbd kbd-sm hidden">⌘</kbd>
      <kbd className="bg-neutral text-neutral-content kbd kbd-sm hidden">K</kbd>
    </label>
  )
}

export default SearchBar;