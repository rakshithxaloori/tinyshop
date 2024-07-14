import ProductDisplayList from "@/components/product-display-list"
import { getWishlist } from "@/lib/cookie/wishlist"
import { getWishlistProductDetails } from "@/lib/storefront"

const WishlistPage = async () => {
  const wishlistItems = await getWishlist()
  if (!wishlistItems) {
    return <div>Wishlist is empty</div>
  }
  let products = await getWishlistProductDetails(wishlistItems)


  return (
    <div className="w-full h-full">
      <h1
        className="mt-lg mb-sm text-3xl font-bold leading-none tracking-tight text-base-content">
        Wishlist
      </h1>
      <ProductDisplayList
        name="Wishlist"
        products={products as any}
      />
    </div>
  )
}

export default WishlistPage