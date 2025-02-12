import { cn } from "@/lib/utils";
import { ShoppingBagIcon } from "lucide-react";

interface QuantityStructureProps {
  quantity: number;
  className?: string | any;
}

const QuantityStructure = ({ quantity, className }: QuantityStructureProps) => {
  return (
    <div className={cn("relative mr-2.5 block h-6 w-6", className)} >
      <ShoppingBagIcon width={24} height={24} className="self-center stroke-nuetral-content fill-nuetral" />
      <span
        className={cn("absolute bottom-0 right-0 inline-flex h-5 w-5 translate-x-1/2 translate-y-1/2 items-center justify-center rounded-full border-2 border-primary-content bg-primary text-primary-content text-center text-xs"
        )}
        aria-label="Items in your cart">
        <span className="sr-only">Items in your cart: </span>
        {quantity}
      </span>

    </div>
  )
}

export default QuantityStructure;