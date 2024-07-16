"use client";

import useCartStore from "@/store/cart"
import { ShoppingBagIcon } from "lucide-react"

import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import CartBagDisplay from "./cart-bag-display";

const EmptyCart = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-3xl font-bold">Your cart is empty</h1>
      <p className="text-lg">Add items to your cart to get started</p>
    </div>
  )
}

const CartListItem = ({ cartItem }: { cartItem: any }) => {
  return (
    <li className="flex justify-between items-center py-2">
      <span className="text-lg">{cartItem.productId}</span>
      <span className="text-lg">${cartItem.quantity}</span>
    </li>
  )
}

const CartList = () => {
  const cartStore = useCartStore()
  const { items } = cartStore

  return (
    <div className="flex flex-col items-center justify-center h-full divide-y divide-primary w-full">

      {
        items.map((item, index) => {
          return (
            <CartListItem key={index} cartItem={item} />
          )
        })
      }
    </div>
  )
}

const Cart = ({
  cartId,
}: {
  cartId: string | null
}) => {
  const cartStore = useCartStore()
  const { items } = cartStore

  const cartItems = items.length
  const cartItemsQty = items.reduce((acc, item) => acc + item.quantity, 0)

  return (
    <Sheet>
      <SheetTrigger>
        <CartBagDisplay quantity={cartItemsQty} />
      </SheetTrigger>
      <SheetContent className="bg-base-200 w-full md:max-w-sm">
        <SheetHeader>
          <SheetTitle>Cart ({cartItemsQty}) | ({cartItems})</SheetTitle>
          {cartItemsQty > 0 ? <CartList /> : <EmptyCart />}
        </SheetHeader>
      </SheetContent>

    </Sheet>
  )
}

export default Cart