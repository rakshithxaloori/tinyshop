"use client";

import { cn } from "@/lib/utils";
import useCartStore from "@/store/cart";
import CheckoutForm from "../checkout-form";

import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { CurrencyString } from "../price/currency-icon";
import Image from "next/image";
import { TCartItem } from "@/types/cart";

const CheckoutCartTable = ({ className }: { className?: string }) => {
  const cartStore = useCartStore();
  return (
    <div className={cn(className)}>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="text-left"><span className="sr-only">Image</span></TableHead>
            <TableHead className="text-left">Product</TableHead>
            <TableHead className="text-right">Price</TableHead>
            <TableHead className="text-right">Quantity</TableHead>
            <TableHead className="text-right">Total</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {cartStore.items.map((item: TCartItem) => (
            <TableRow key={item.id}>
              <TableCell className="relative h-24 w-24">
                <Image
                  src={item.image}
                  alt={item.name}
                  // fill
                  width={96}
                  height={96}
                  className="aspect-square rounded-lg"
                />
              </TableCell>
              <TableCell className="text-left">
                <span>{item.name}</span>
                {item.variantName && <span className="text-sm text-base-content/70 line-clamp-1">{item.variantName}</span>}

              </TableCell>
              <TableCell className="text-right"><CurrencyString currency="inr" />{" "}{item.price}</TableCell>
              <TableCell className="text-right">{item.quantity}</TableCell>
              <TableCell className="text-right">
                <CurrencyString currency="inr" />{" "}{Number(item.price) * item.quantity}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>

        <TableFooter>
          <TableRow>
            <TableCell colSpan={4} className="text-right">Total</TableCell>
            <TableCell className="text-right">
              <CurrencyString currency="inr" />{" "}{cartStore.items.reduce((acc, item) => acc + (item.price as number) * item.quantity, 0)}
            </TableCell>
          </TableRow>
        </TableFooter>

      </Table>
    </div>
  )
}

const CheckoutCartSection = () => {
  return (
    <div className="sticky top-[7rem]">
      <h1 className="mb-4 text-3xl font-bold leading-none tracking-tight">Your Cart</h1>
      <CheckoutCartTable />
    </div>
  )
}

const CheckoutPage = () => {
  return (
    <div className="grid lg:grid-cols-1 lg:grid-cols-12 lg:gap-x-8 w-fit">
      <div className="my-lg lg:col-span-7">
        <CheckoutCartSection />
      </div>
      <CheckoutForm className="lg:col-span-5" />
    </div>
  )
}

export default CheckoutPage