"use client";
import { addToWishlist, hasWishlistItem, removeFromWishlist } from "@/lib/cookie/wishlist";
import { cn } from "@/lib/utils";
import { TProduct } from "@/types/product"
import { HeartIcon } from "lucide-react"
import { useCallback, useEffect, useState } from "react";

const WishlistItem = ({ id, className }: {
  id: string;
  className?: string;
}) => {
  const [wish, setWish] = useState<boolean | null>(null)

  const handleChange = useCallback(
    async (e: React.MouseEvent<HTMLLabelElement>, currentWish: boolean | null) => {
      e.preventDefault()
      e.stopPropagation()
      if (currentWish === null) return
      setWish(!currentWish)
      if (!currentWish) {
        await addToWishlist(id)
      } else {
        await removeFromWishlist(id)
      }
    }
    , [id])

  useEffect(() => {
    // Check if product is in wishlist
    // If it is, setWish to true
    // else setWish to false
    async function fetchWishListCookie() {
      const hasWish = await hasWishlistItem(id)
      setWish(hasWish)
    }
    fetchWishListCookie()
  }, [id])

  return (
    <div className={cn("absolute top-0 right-0 m-0 mt-2 mr-2 p-0", className)}>
      <label className={cn("swap swap-flip p-0 m-0",
        { "swap-active": wish }
      )}
        onClick={(e) => handleChange(e, wish)}
      >
        <HeartIcon size={24}
          fillOpacity={0.5}
          className="swap-on fill-primary stroke-primary" />
        <HeartIcon size={24}
          className="swap-off stroke-primary/80"
        />
      </label>
    </div>
  )
}

export default WishlistItem