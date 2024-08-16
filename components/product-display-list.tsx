"use client";

import { TProduct } from "@/types/product";
import ProductCard from "./product/card-v1";
import { ProductLayout } from "./product/card-structure";

interface ProductDisplayListProps {
  name: string;
  products: TProduct[];
  layout: ProductLayout;
}

const ProductDisplayList = (
  { name, products, layout }: ProductDisplayListProps
) => {
  return (

    <div className="my-lg grid grid-cols-2 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {
        products.map((product) => (
          <ProductCard key={product.name} product={product}
            fallbackOptions={{
              image: "https://images.unsplash.com/photo-1620987278429-ab178d6eb547?q=80&w=2825&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            }}
            layout={layout}
          />
        ))
      }
    </div>
  )
}

export default ProductDisplayList