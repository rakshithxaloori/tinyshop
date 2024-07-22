"use client";

import useCartStore from "@/store/cart"
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import CartBagDisplay from "./cart-bag-display";
import { TCartItem, TCartItemDisplay, TItemChain } from "@/types/cart";
import Image from "next/image";
import { Button } from "./ui/button";
import { CurrencyString } from "./price/currency-icon";
import { MinusCircleIcon, MinusIcon, PlusCircleIcon, PlusIcon } from "lucide-react";

const EmptyCart = () => {
  return (
    <div className="flex flex-col flex-1 justify-start pt-4">
      <h1 className="text-3xl font-bold">Your cart is empty</h1>
      <p className="text-lg">Add items to your cart to get started</p>
    </div>
  )
}

const CartListItem = ({ cartItem }: { cartItem: TCartItem }) => {
  const { image, name, price, currency, quantity } = cartItem
  const { addItem, removeItem } = useCartStore()

  const itemChain: TItemChain = cartItem as TItemChain
  const displayItem: TCartItemDisplay = cartItem as TCartItemDisplay

  return (
    <div className="grid grid-cols-1 md:grid-cols-[20%_1fr_auto] gap-3 w-full bg-base-200 max-h-24">
      <div className="relative w-full aspect-square">
        <Image
          src={image}
          alt={name}
          fill
          className="object-cover rounded-lg"
        />
      </div>
      <div className="flex flex-col gap-0.5 text-sm mt-2">
        <span className="text-sm font-medium line-clamp-2">
          {name}
        </span>
        <span className="text-sm text-base-content/70">
          <CurrencyString currency={currency} />
          {price}
        </span>
      </div>
      <div className="flex flex-row gap-1 items-center px-1 align-end">
        <button className="btn btn-circle btn-sm p-0 border-neutral/50 hover:border-neutral/80 border-2" onClick={() => removeItem(itemChain)}>
          <MinusIcon />
        </button>
        <span className="p-2 text-sm">{quantity}</span>
        <button className="btn btn-circle btn-sm p-0 border-neutral/50 hover:border-neutral/80 border-2" onClick={() => addItem(itemChain, displayItem, 1)} >
          <PlusIcon />
        </button>
      </div>
    </div>

  )
}

const CartList = () => {
  const cartStore = useCartStore()
  const { items } = cartStore

  return (
    <div className="flex flex-col gap-2 w-full justify-start max-h-full overflow-y-scroll">
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
  const { items, clearCart } = cartStore

  const cartItems = items.length
  const cartItemsQty = items.reduce((acc, item) => acc + item.quantity, 0)

  const onClearClick = (e: any) => {
    e.preventDefault()
    e.stopPropagation();
    clearCart()
  }

  const cartItemsTotal = items.reduce((acc, item) => acc + (item.price as number) * item.quantity, 0)
  const cartItemsTotalCurrency = (items[0]?.currency || 'INR')

  return (
    <Sheet>
      <SheetTrigger>
        <CartBagDisplay quantity={cartItemsQty} />
      </SheetTrigger>
      <SheetContent className="flex flex-col overflow-y-hidden bg-base-200 w-full md:max-w-md">
        <SheetHeader>
          <SheetTitle>Cart ({cartItemsQty})</SheetTitle>
          <a className="link link-error" onClick={onClearClick} >Clear</a>
        </SheetHeader>
        <div className="flex flex-1 overflow-y-scroll w-full">
          {cartItemsQty > 0 ? <CartList /> : <EmptyCart />}
        </div>

        <div className="border-t border-neutral py-4 sm:px-6">
          <div className="flex justify-between text-base font-medium text-base-content">
            <p>Total</p>
            <span>
              <CurrencyString currency={cartItemsTotalCurrency} />
              {" "}{cartItemsTotal}
            </span>
          </div>
          <p className="mt-sm text-sm text-base-content">Shipping and taxes will be added at the next step</p>
          <button className="btn btn-primary btn-block mt-md text-primary-content" disabled={cartItems === 0}>
            Go to payment
          </button>
        </div>
      </SheetContent>

    </Sheet>
  )
}

export default Cart