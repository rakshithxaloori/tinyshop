"use client";

import { TProduct } from "@/types/product";
import ProductCard from "./product/card-v1";

interface ProductDisplayHorizonalListProps {
  name: string;
  products: TProduct[];
}

const ProductDisplayHorizonalList = (
  { name, products }: ProductDisplayHorizonalListProps
) => {
  return (

    <div className="flex flex-row overflow-x-hidden relative -px-md">
      <div className="my-lg flex flex-row overflow-x-auto gap-x-1 snap-x snap-mandatory scrollbar-hide relative">
        {products.map((product) => (
          <div key={product.name} className="flex-none w-1/2 md:w-1/4 snap-start">
            <ProductCard
              product={product}
              fallbackOptions={{
                image: "https://images.unsplash.com/photo-1620987278429-ab178d6eb547?q=80&w=2825&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              }}
            />
          </div>
        ))}
      </div>
      <div className="absolute left-0 top-0 bottom-0 w-[1rem] md:w-[1.5rem] bg-gradient-to-r from-base-100 to-transparent pointer-events-none"></div>
      <div className="absolute right-0 top-0 bottom-0 w-[1rem] md:w-[1.5rem] bg-gradient-to-l from-base-100 to-transparent pointer-events-none"></div>
    </div>
  )
}

export default ProductDisplayHorizonalList