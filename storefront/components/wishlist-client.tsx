"use client";
import { clearWishlist } from "@/lib/cookie/wishlist"
import { TrashIcon } from "lucide-react"

export const WishlistClearButton = () => {
  const onClearWishlist = async () => {
    await clearWishlist()
  }

  return (
    <button className="btn btn-error"
      onClick={onClearWishlist}
    >
      <TrashIcon className="stroke-error-content" fillOpacity={0.5} />
      <span className="hidden md:visible" >Clear Wishlist</span>
    </button>
  )
}