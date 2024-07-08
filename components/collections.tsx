import GlassProductCard from "./glass-product-card";
import ProductCard from "./product-card";

interface CollectionsProps {
  name: string;
  products: TProduct[];
}

const Collections = (
  { name, products }: CollectionsProps
) => {
  return (
    <div>
      <h1>{name}</h1>
      <div className="grid grid-cols-1 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 md:gap-4">
        {
          products.map((product) => (
            // <ProductCard key={product.name} product={product} />
            <GlassProductCard key={product.name} product={product} />
          ))
        }
      </div>
    </div>
  )
}

export default Collections