"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { Input } from "@/components/ui/input"


const SearchBar = () => {
  const pathname = usePathname();
  const searchParam = useSearchParams().get("q");
  console.log("searchParam", searchParam);
  const [search, setSearch] = useState<string | null>(null);
  const historyPath = useRef("");

  const router = useRouter();
  useEffect(() => {
    if (pathname === "/search" || search !== null && search.length > 0) {
      if (search !== null && search.length > 0) {
        router.push(`/search?q=${search}`);
      } else {
        if (search !== null) {
          console.log("search is empty, calling /demo");
          router.push(historyPath.current || "/demo");
        }
      }
    }
  }, [search, router, pathname]);

  useEffect(() => {
    if (searchParam !== null && pathname === "/search") {
      setSearch(searchParam);
    } else {
      setSearch("");
    }
  }, [searchParam, pathname]);

  const handleSearchInput = (e: any) => {
    e.preventDefault();
    if (search === null || search.length === 0) {
      historyPath.current = pathname;
    }
    setSearch(e.target.value);
  }

  return (
    <label className="input input-bordered flex items-center gap-2">
      <input type="text" className="grow" placeholder="Search products..."
        value={search || ""}
        onChange={handleSearchInput}
      />
      <kbd className="kbd kbd-sm">⌘</kbd>
      <kbd className="kbd kbd-sm">K</kbd>
    </label>
  )
}

export default SearchBar;