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
import { CurrencyString } from "./price/currency-icon";
import { CartList, EmptyCartList } from "./cart-list";
import { useRouter } from "next/navigation";

const Cart = () => {
  const cartStore = useCartStore()
  const { items, clearCart } = cartStore
  const router = useRouter()

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
        <SheetHeader >
          <SheetTitle>Cart ({cartItemsQty})</SheetTitle>
          <a className="link link-error" onClick={onClearClick} >Clear</a>
        </SheetHeader>
        <div className="flex flex-1 overflow-y-scroll w-full">
          {cartItemsQty > 0 ? <CartList /> : <EmptyCartList />}
        </div>

        <div className="border-t border-secondary-content py-4 sm:px-6">
          <div className="flex justify-between text-base font-medium text-base-content">
            <p>Total</p>
            <span>
              <CurrencyString currency={cartItemsTotalCurrency} />
              {" "}{cartItemsTotal}
            </span>
          </div>
          <p className="mt-sm text-sm text-base-content">Shipping and taxes will be added at the next step</p>
          <button className="btn btn-secondary btn-block mt-md" disabled={cartItems === 0}
            onClick={() => {
              router.push('/checkout')
            }}
          >
            Go to payment
          </button>
        </div>
      </SheetContent>

    </Sheet>
  )
}

export default Cart