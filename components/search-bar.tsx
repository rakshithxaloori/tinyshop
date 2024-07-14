"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";


const SearchBar = () => {
  const pathname = usePathname();
  const searchParam = useSearchParams().get("q");
  const [search, setSearch] = useState<string | null>(null);
  const historyPath = useRef("");

  console.log("search", search);
  console.log("pathname", pathname);
  console.log("searchParam", searchParam);
  console.log("historyPath", historyPath.current);

  const router = useRouter();
  useEffect(() => {
    if (pathname === "/search" || search !== null && search.length > 0) {
      if (search !== null && search.length > 0) {
        router.push(`/search?q=${search}`);
      } else {
        if (search !== null) {
          router.push(historyPath.current || "/");
        }
      }
    } else {
      console.log("not in the search path", pathname);
      setSearch((s) => "");
    }
  }, [search, router, pathname]);

  const handleSearchInput = (e: any) => {
    e.preventDefault();
    if (search === null || search.length === 0) {
      historyPath.current = pathname;
    }
    setSearch(e.target.value);
  }

  return (
    <label className="input input-bordered flex bg-secondary items-center gap-2">
      <input type="text" className="grow text-secondary-content" placeholder="Search products..."
        value={search || ""}
        onChange={handleSearchInput}
      />
      <kbd className="bg-secondary kbd kbd-sm">⌘</kbd>
      <kbd className="bg-secondary kbd kbd-sm">K</kbd>
    </label>
  )
}

export default SearchBar;