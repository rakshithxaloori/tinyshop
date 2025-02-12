"use client";

import Image from "next/image";
import { TCartItem, TCartItemDisplay, TItemChain } from "@/types/cart";
import useCartStore from "@/store/cart"
import { CurrencyString } from "./price/currency-icon";

import { MinusIcon, PlusIcon } from "lucide-react";


const CartListItem = ({ cartItem }: { cartItem: TCartItem }) => {
  const { image, name, price, currency, quantity, variantName, isSubscription: sub } = cartItem
  const displayPrice = (Number(price) / 100).toString()
  const { addItem, removeItem } = useCartStore()

  const itemChain: TItemChain = cartItem as TItemChain
  const displayItem: TCartItemDisplay = cartItem as TCartItemDisplay

  const handleAddItem = (e: any) => {
    e.preventDefault()
    e.stopPropagation()
    addItem(itemChain, displayItem, 1)
  }

  const handleRemoveItem = (e: any) => {
    e.preventDefault()
    e.stopPropagation()
    removeItem(itemChain)
  }

  return (
    <div className="grid grid-cols-[20%_1fr_auto] gap-3 w-full h-fit p-sm">
      <div className="relative max-h-fit max-w-24">
        <Image
          src={image}
          alt={name}
          fill
          className="object-cover rounded-lg"
        />
      </div>
      <div className="flex flex-col gap-0.5 text-sm mt-2">
        <span className="text-sm font-medium line-clamp-1">
          {name}
        </span>
        {variantName && <span className="text-sm text-base-content/70 line-clamp-1">{variantName}</span>}
        <span className="text-sm text-base-content/70">
          <CurrencyString currency={currency} />
          {displayPrice}
          {sub && <span className="text-sm font-normal text-base-content/60 self-align-end ml-xs">/month</span>}
        </span>
      </div>
      <div className="flex flex-row gap-1 items-center px-1 align-end">
        <button className="btn btn-circle btn-sm p-0 border-neutral border-2" onClick={handleRemoveItem}>
          <MinusIcon />
        </button>
        <span className="p-2 text-sm">{quantity}</span>
        <button className="btn btn-circle btn-sm p-0 border-neutral border-2" onClick={handleAddItem} >
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
    <div className="flex flex-col gap-2 w-full justify-start max-h-full overflow-y-scroll divide-y-2 border-y-primary">
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

const EmptyCartList = () => {
  return (
    <div className="flex flex-col flex-1 justify-start pt-4">
      <h1 className="text-3xl font-bold">Your cart is empty</h1>
      <p className="text-lg">Add items to your cart to get started</p>
    </div>
  )
}

export { CartList, CartListItem, EmptyCartList }