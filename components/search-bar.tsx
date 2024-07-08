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

    <Input type="email" placeholder="Search products..."
      value={search || ""}
      onChange={handleSearchInput}
      className="w-full outline-none bg-transparent text-gray-600 text-sm" />

  )
}

export default SearchBar;