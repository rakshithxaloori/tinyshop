import WishlistPage from "@/components/pages/wishlist-page"
import { getWishlist } from "@/lib/cookie/wishlist"
import { getWishlistProductDetails } from "@/lib/storefront"

const WishlistItemsDisplayPage = async () => {
  const wishlistItems = await getWishlist()
  if (!wishlistItems) {
    return <div>Wishlist is empty</div>
  }
  let products = await getWishlistProductDetails(wishlistItems)

  return (
    <WishlistPage products={products} />
  )
}

export default WishlistItemsDisplayPage