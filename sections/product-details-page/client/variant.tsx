"use client";

import PriceCard from "@/components/price/price-card-v1";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { MinusIcon, PlusIcon, ShoppingBagIcon } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { useVariant } from "../hook/variant";

const SingleOptionComponent = ({
  option,
  selectedOption,
  onSelect,
  disabled,
  className,
  ...props
}: {
  option: any,
  selectedOption: any,
  onSelect: any,
  disabled: boolean,
  className: string,
  props: any
}) => {
  return (
    <div>
      <button
        onClick={() => onSelect(option)}
        disabled={disabled}
        className={cn(
          "w-full py-2 px-4",
          selectedOption === option ? "bg-primary-500 text-white" : "bg-base-100 text-black",
          disabled ? "cursor-not-allowed" : "cursor-pointer",
          className
        )}
        {...props}
      >
        {option}
      </button>
    </div>
  )
}

const MultiOptionComponent = () => {
  /* TODO: implement it */
}

// Quantity Selector and the Add to Cart Button
const AddToCart = ({ config }:
  {
    config: any
  }
) => {
  const { shouldAnimateButton } = config
  return (
    <div className="flex flex-row mt-2 gap-2">
      <QuantitySelector />
      <Button
        className={cn("btn flex-1 text-primary-content",
          shouldAnimateButton ? "animate-buttonheartbeat" : "",
          "hover:animate-hover-pulse"
        )}>
        <ShoppingBagIcon />
        <p>Add to Cart</p>
      </Button>
    </div>
  )
}

const QuantitySelector = () => {
  const [quantity, setQuantity] = useState(1)

  const handleIncrement = () => {
    setQuantity(quantity + 1)
  }

  const handleDecrement = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1)
    }
    // if you can't decrement, you can show a toast message
  }

  return (
    <div className="flex flex-row justify-center items-center border-2 rounded-sm border-primary">
      <Button
        variant="ghost"
        onClick={handleDecrement}
        className="bg-transparent hover:bg-transparent hover:text-primary-content px-0 text-primary"
      >
        <MinusIcon />
      </Button>
      <span className="p-2 px-3">{quantity}</span>
      <Button
        variant="ghost"
        onClick={handleIncrement}
        className="bg-transparent hover:bg-transparent
         hover:text-primary-content px-0 text-primary
         transition-all"
      >
        <PlusIcon className="p-0 h-6 w-6" />
      </Button>
    </div>
  )
}

const VariantItem = ({ variant, selectedVariant, onSelect }: {
  variant: any; selectedVariant: any;
  onSelect: Function
}) => {
  // display the one_time of the variant
  const { prices } = variant;
  const priceAmount = prices.data[0].unit_amount
  const priceCurrency = prices.data[0].currency
  const isSelected = useMemo(() => selectedVariant.id === variant.id, [selectedVariant, variant])
  return (
    <div className={cn("flex flex-row min-w-full item-center h-full p-2 mt-2",
      isSelected ? "border-2 border-primary" : "border-2 border-primary",
      isSelected ? "border-opacity-100" : "border-opacity-0",
      "hover:border-primary hover:border-opacity-100 cursor-pointer transition-all",
      isSelected && "cursor-not-allowed",
    )}
      onClick={() => onSelect(variant)}
    >
      <h1 className="text-lg font-bold">{variant.name}</h1>
      <div className="grow"></div>
      <PriceCard price={priceAmount} currency={priceCurrency} />
    </div>
  )
}
const VariantSelector = ({ product }: { product: any }) => {
  const variantInfo = product.variants.data
  const [selectedVariant, setSelectedVariant] = useState(variantInfo[0])
  const { setVariant } = useVariant();

  useEffect(() => {
    setVariant(selectedVariant)
  }, [setVariant, selectedVariant])

  const handleSelectVariant = (localVariant: any) => {
    setSelectedVariant(localVariant)
  }

  return (
    <div className={cn("flex flex-col w-full overflow-x-scroll",
      variantInfo.length === 1 && "hidden"
    )}>
      {
        variantInfo.map((variant: any, index: number) => {
          return (
            <VariantItem
              key={index}
              {...{ variant, selectedVariant, }}
              onSelect={handleSelectVariant}
            />
          )
        })
      }
    </div>
  )
}

const PriceAndAddToCardComponent = ({
  product
}: {
  product: any
}

) => {
  const { option, variant } = product

  return (
    <div>
      <AddToCart config={{
        shouldAnimateButton: false
      }} />
    </div>
  )
}

const PriceDisplay = ({
  cx
}: {
  cx?: string
}) => {
  const { variant } = useVariant()
  if (!variant) {
    return null
  }
  const { prices } = variant;
  const priceAmount = prices.data[0].unit_amount
  const priceCurrency = prices.data[0].currency
  const comparePrice = prices.data[0].unit_compare_amount


  return (
    <div className={cn("flex flex-row items-center",
      !!cx && cx,
    )}
    >
      <PriceCard price={priceAmount} currency={priceCurrency}
        comparePrice={comparePrice}
      />
    </div>

  )
}

export {
  SingleOptionComponent,
  MultiOptionComponent,
  PriceAndAddToCardComponent,
  VariantSelector,
  PriceDisplay
}