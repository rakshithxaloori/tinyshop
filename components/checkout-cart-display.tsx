"use client";

import { cn } from "@/lib/utils";
import useCartStore from "@/store/cart";

import Image from "next/image";
import { TCartItem } from "@/types/cart";

import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { CurrencyString } from "./price/currency-icon";

const CheckoutCartTable = () => {
  const cartItems = useCartStore((state) => state.items);
  const cartTotal = cartItems.reduce((acc, item) => acc + (item.price as number) * item.quantity, 0) / 100

  return (
    <div>
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
          {cartItems.map((item: TCartItem) => (
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
              <TableCell className="text-right"><CurrencyString currency="inr" />{" "}{Number(item.price) / 100}</TableCell>
              <TableCell className="text-right">{item.quantity}</TableCell>
              <TableCell className="text-right">
                <CurrencyString currency="inr" />{" "}{Number(item.price) / 100 * item.quantity}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>

        <TableFooter>
          <TableRow>
            <TableCell colSpan={4} className="text-right">Total</TableCell>
            <TableCell className="text-right">
              <CurrencyString currency="inr" />{" "}{cartTotal}
            </TableCell>
          </TableRow>
        </TableFooter>

      </Table>
    </div>
  )
}

const CheckoutCartDisplay = ({ className }: { className?: string }) => {
  return (
    <div className={cn("my-lg lg:col-span-7", className)}>
      <div className="sticky top-[7rem]">
        <h1 className="mb-4 text-3xl font-bold leading-none tracking-tight">Your Cart</h1>
        <CheckoutCartTable />
      </div>
    </div>
  )
}


export default CheckoutCartDisplay