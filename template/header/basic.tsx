import Cart from "@/components/cart";
import SearchBar from "@/components/search-bar";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { Suspense } from "react";

const BasicHeader = ({
  className
}: {
  className?: string;
}) => {
  return (
    <div className={cn("h-[8vh] flex w-full py-4 px-8 items-center justify-start gap-2 sticky top-0 left-0 z-30", className)}
      data-theme="coffee"
    >
      <section id="basic-header-name">
        <Link href="/demo">
          <h1 className="text-2xl">Your Store</h1>
        </Link>
      </section>
      <section id="basic-header-nav" className="flex space-x-4">
        <a href="#" className="">Shop</a>
        <a href="#" className="">About</a>
      </section>
      <section id="basic-header-right" className="flex space-x-4 min-w-lg ml-auto items-center">
        <section id="basic-header-search" className="flex space-x-4 ml-auto">
          <Suspense fallback={<div>Loading...</div>}>
            <SearchBar />
          </Suspense>
        </section>
        <section id="basic-header-cart" className="flex space-x-4">
          <Cart />
        </section>

      </section>
    </div>
  );
}

export default BasicHeader;