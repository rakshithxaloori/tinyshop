import WishlistPage from "@/components/pages/wishlist-page"
import { getWishlist } from "@/lib/cookie/wishlist"
import { getWishlistProductDetails } from "@/lib/storefront"
import { Metadata } from "next";

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME! as string || "tinyshop";
export const metadata: Metadata = {
  title: `Wishlist - ${shopName}`,
  description: "Search for products",
};

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