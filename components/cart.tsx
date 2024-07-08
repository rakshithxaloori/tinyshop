"use client";

import useCartStore from "@/store/cart"
import { ShoppingBagIcon } from "lucide-react"

const Cart = () => {
  const cartStore = useCartStore()
  const { cart } = cartStore
  const cartItems = Object.values(cart).reduce((acc, val) => acc + Object.values(val).reduce((acc, val) => acc + val, 0), 0)
  return (
    <a className="relative mr-2.5 block h-6 w-6" >
      <ShoppingBagIcon width={24} height={24} className="self-center" />
      <span
        className="absolute bottom-0 right-0 inline-flex h-5 w-5 translate-x-1/2 translate-y-1/2 items-center justify-center rounded-full border-2 bg-white text-center text-xs"
        aria-label="Items in your cart">
        <span className="sr-only">Items in your cart: </span>
        {cartItems}
      </span>
    </a>
  )
}

export default Cart