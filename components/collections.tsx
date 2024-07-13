// import GlassProductCard from "./glass-product-card";
// import ProductCard from "./product-card";
import ProductCard from "./product/card-v1";

interface CollectionsProps {
  name: string;
  products: TProduct[];
}

const Collections = (
  { name, products }: CollectionsProps
) => {
  return (
    <div className="my-lg">
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 md:gap-4">
        {
          products.map((product) => (
            <ProductCard key={product.name} product={product}
              fallbackOptions={{
                image: "https://images.unsplash.com/photo-1620987278429-ab178d6eb547?q=80&w=2825&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              }}
            />
          ))
        }
      </div>
    </div>
  )
}

export default Collections