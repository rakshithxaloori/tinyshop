"use client";

import useCartStore from "@/store/cart"

import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerPortal,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer"

import { useState } from "react";
import CartBagDisplay from "./cart-bag-display";
import { CartList, EmptyCartList } from "./cart-list";
import { CurrencyString } from "./price/currency-icon";



const CartV2 = () => {
  const cartStore = useCartStore()
  const { items, clearCart } = cartStore

  const cartItems = items.length;
  const cartItemsQty = items.reduce((acc, item) => acc + item.quantity, 0);


  const onClearClick = (e: any) => {
    e.preventDefault()
    e.stopPropagation();
    clearCart()
  }

  const cartItemsTotal = items.reduce((acc, item) => acc + (item.price as number) * item.quantity, 0)
  const cartItemsTotalCurrency = (items[0]?.currency || 'INR')

  const [isOpen, setOpen] = useState<boolean>(false);


  return (
    <Drawer direction="right" open={isOpen} onOpenChange={setOpen}>
      <DrawerTrigger>
        <CartBagDisplay quantity={cartItemsQty} />
      </DrawerTrigger>
      <DrawerContent className="h-full w-full justify-end bg-base-100 text-base-content">
        <DrawerHeader className="flex flex-row justify-between px-md">
          <DrawerTitle>
            <span>Cart ({cartItemsQty})</span>
          </DrawerTitle>
          <a className="link link-error" onClick={onClearClick} >Clear</a>
        </DrawerHeader>
        <div className="flex flex-1 overflow-y-scroll w-full px-md">
          {cartItemsQty > 0 ? <CartList /> : <EmptyCartList />}
        </div>
        <div className="border-t border-secondary-content py-4 sm:px-6 mt-sm px-md">
          <div className="flex justify-between text-base font-medium text-base-content">
            <p>Total</p>
            <span>
              <CurrencyString currency={cartItemsTotalCurrency} />
              {" "}{cartItemsTotal}
            </span>
          </div>
          <p className="mt-sm text-sm text-base-content">Shipping and taxes will be added at the next step</p>
          <button className="btn btn-secondary btn-block mt-md" disabled={cartItems === 0}>
            Go to payment
          </button>
        </div>
      </DrawerContent>
    </Drawer>
  )
}


export default CartV2