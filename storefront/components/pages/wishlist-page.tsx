import ProductDisplayList from "@/components/product-display-list"
import { WishlistClearButton } from "@/components/wishlist-client"
import { getProductLayoutDetails } from "@/lib/storefront";

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME! as string || "tinyshop";


const WishlistPage = async ({
  products
}: {
  products: any
}) => {
  const mongoLayout = await getProductLayoutDetails(shopName);
  const cardLayout = mongoLayout?.layout || null;
  if (!cardLayout) {
    throw new Error('No layout found for the brand');
  }


  return (
    <div className="min-w-full h-full grid grid-rows-[auto_1fr] px-lg md:px-xl">
      <div className="flex flex-row w-full grow items-center justify-between mt-lg mb-sm">
        <h1
          className="text-3xl font-bold leading-none tracking-tight text-base-content">
          Wishlist
        </h1>
        <WishlistClearButton />
      </div>
      <ProductDisplayList
        name="Wishlist"
        products={products}
        layout={cardLayout}
      />
    </div>
  )
}

export default WishlistPage