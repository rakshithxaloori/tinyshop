"use client";

import useCartStore from "@/store/cart"
import { ShoppingBagIcon } from "lucide-react"
import { useCartModal } from "./hooks/cart";

import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"

const EmptyCart = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-3xl font-bold">Your cart is empty</h1>
      <p className="text-lg">Add items to your cart to get started</p>
    </div>
  )
}

const CartList = () => {
  const cartStore = useCartStore()
  const { cart } = cartStore

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <ul className="divide-y divide-primary w-full">
        {Object.entries(cart).map(([productId, product]) => {
          return (
            <li key={productId} className="flex justify-between items-center p-2">
              <span>{product.name}</span>
              <span>{product.quantity}</span>
              <span>{product.price}</span>
            </li>
          )
        })}
      </ul>
    </div>
  )

}

const Cart = () => {
  const cartStore = useCartStore()
  const { cart } = cartStore
  if (!cart) return null
  const cartItems = 0

  return (
    <Sheet>
      <SheetTrigger>
        <div className="relative mr-2.5 block h-6 w-6" >
          <ShoppingBagIcon width={24} height={24} className="self-center" />
          <span
            className="absolute bottom-0 right-0 inline-flex h-5 w-5 translate-x-1/2 translate-y-1/2 items-center justify-center rounded-full border-2 bg-white text-center text-xs"
            aria-label="Items in your cart">
            <span className="sr-only">Items in your cart: </span>
            {cartItems}
          </span>
        </div>
      </SheetTrigger>
      <SheetContent className="bg-base-200 w-full md:max-w-sm">
        <SheetHeader>
          <SheetTitle>Cart ({cartItems})</SheetTitle>
          <SheetDescription>
            {cartItems > 0 ? <CartList /> : <EmptyCart />}
          </SheetDescription>
        </SheetHeader>
      </SheetContent>

    </Sheet>
  )
}

export default Cart