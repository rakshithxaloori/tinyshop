import ProductDisplayList from "@/components/product-display-list"
import { WishlistClearButton } from "@/components/wishlist-client"


const WishlistPage = async ({
  products
}: {
  products: any
}) => {



  return (
    <div className="w-full h-full grid grid-rows-[auto_1fr]">
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
      />
    </div>
  )
}

export default WishlistPage