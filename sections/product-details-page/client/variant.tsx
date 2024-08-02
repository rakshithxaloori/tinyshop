"use client";

import PriceCard from "@/components/price/price-card-v1";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { MinusIcon, PlusIcon, ShoppingBagIcon } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useVariant } from "../hook/variant";
import useCartStore from "@/store/cart";
import dynamic from "next/dynamic";

const disableOneTime = process.env.NEXT_PUBLIC_DISABLE_ONE_TIME! === "true";

const NoSSRCartBagDisplay = dynamic(() => import("@/components/cart-bag-display"), {
  ssr: false,
  loading: () => <div className="mx-2.5 ml-2 block h-6 w-6 animate-spin border-2 rounded-full border-base-300 border-t-primary" />
});

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
const AddToCart = ({ config, product }:
  {
    config: any;
    product: any;
  }
) => {
  const [quantity, setQuantity] = useState<number>(1)
  const { price: selectedPrice } = useVariant();
  const { shouldAnimateButton } = config
  const { addItem } = useCartStore()

  const handleIncrement = () => {
    setQuantity(quantity + 1)
  }

  const handleDecrement = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1)
    }
    // if you can't decrement, you can show a toast message
  }

  const cartItemChain = {
    productId: product.id,
    variantId: selectedPrice?.variant || "",
    priceId: selectedPrice?.id || "",
  }

  const cartItemDisplay = {
    image: product.images.length ? product.images[0] : "",
    name: product.name,
    variantName: selectedPrice?.variantName || "",
    price: selectedPrice?.unit_amount || 0,
    currency: selectedPrice?.currency || "",
    isSubscription: selectedPrice?.type === "subscription",
  }

  const handleAddToCart = (e: any) => {
    e.preventDefault();
    e.stopPropagation();
    addItem(cartItemChain, cartItemDisplay, quantity)
    setQuantity(1)
  }

  return (
    <div className="flex flex-row mt-2 gap-2">
      <QuantitySelector
        quantity={quantity}
        onIncrement={handleIncrement}
        onDecrement={handleDecrement}
      />
      <Button
        className={cn("btn flex-1 text-primary-content",
          shouldAnimateButton ? "animate-buttonheartbeat" : "",
          "hover:animate-hover-pulse"
        )}
        onClick={handleAddToCart}
      >
        <ShoppingBagIcon />
        <p>Add to Cart</p>
      </Button>
    </div>
  )
}

const QuantitySelector = ({
  quantity,
  onIncrement,
  onDecrement,
}:
  {
    quantity: number,
    onIncrement: any,
    onDecrement: any,
  }) => {
  return (
    <div className="flex flex-row justify-center items-center border-2 rounded-sm border-primary">
      <Button
        variant="ghost"
        onClick={onDecrement}
        className="bg-transparent hover:bg-transparent hover:text-primary-content px-0 text-primary"
      >
        <MinusIcon />
      </Button>
      <span className="p-2 px-3">{quantity}</span>
      <Button
        variant="ghost"
        onClick={onIncrement}
        className="bg-transparent hover:bg-transparent
         hover:text-primary-content px-0 text-primary
         transition-all"
      >
        <PlusIcon className="p-0 h-6 w-6" />
      </Button>
    </div>
  )
}

const PriceItem = ({ price, selectedPrice, onSelect }: {
  price: any; selectedPrice: any;
  onSelect: Function;
}) => {
  const isSelected = useMemo(() => selectedPrice.id === price.id, [selectedPrice, price])
  const { getPrice } = useCartStore()
  const cartVariantQty = getPrice(price.id).quantity
  const isSub = price.type === "subscription"

  const priceAmount = price.unit_amount
  const priceCurrency = price.currency

  return (
    <div className={cn("flex flex-row min-w-full item-center h-full p-2 mt-2",
      isSelected ? "border-2 border-primary" : "border-2 border-primary",
      isSelected ? "border-opacity-100" : "border-opacity-0",
      "hover:border-primary hover:border-opacity-100 cursor-pointer transition-all",
      // isSelected && "cursor-not-allowed",
    )}
      onClick={() => onSelect(price)}
    >
      <div className="flex flex-row flex-1">
        <span className={cn("text-lg font-bold")}>{price.variantName}</span>
        <div className="grow"></div>
        <PriceCard price={priceAmount} currency={priceCurrency} isSubscription={price.type === "subscription"} />
        <NoSSRCartBagDisplay quantity={cartVariantQty} cx="ml-2" />
      </div>
    </div>
  )
}

const PriceSelector = ({ product }: { product: any }) => {
  // flatten the prices array

  const variantInfo = product.variants.data

  let flattenedPrices = variantInfo.map((variant: any) => {
    const prices = variant.prices.data
    return prices.map((price: any) => {
      return {
        ...price,
        variantName: variant.name
      }
    })
  })

  flattenedPrices = flattenedPrices.flat()

  // if disable one time is set, filter out the one time prices
  if (disableOneTime) {
    flattenedPrices = flattenedPrices.filter((price: any) => price.type === "subscription")
  }

  const [selectedPrice, setSelectedPrice] = useState(flattenedPrices[0])
  const { setPrice } = useVariant();
  const { getProduct } = useCartStore()
  const cartProductQty = getProduct(product.id).quantity

  useEffect(() => {
    setPrice(selectedPrice)
  }, [setPrice, selectedPrice])

  const handleSelectPrice = (localPrice: any) => {
    setSelectedPrice(localPrice)
  }

  return (
    <div className={cn("flex flex-col w-full overflow-x-scroll mt-md",
      (flattenedPrices.length === 1 && cartProductQty === 0) && "hidden"
    )}>
      {
        flattenedPrices.map((price: any, index: number) => {
          return (
            <PriceItem
              key={index}
              price={price}
              selectedPrice={selectedPrice}
              onSelect={handleSelectPrice}
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
  return (
    <div>
      <AddToCart config={{
        shouldAnimateButton: false
      }}
        product={product}
      />
    </div>
  )
}

const PriceDisplay = ({
  cx
}: {
  cx?: string
}) => {
  const { price } = useVariant()
  // check if it's a subscription variant
  const isSubscription = price.type === "subscription"
  let displayPriceAmount = price.unit_amount
  const displayPriceCurrency = price.currency
  const displayComparePrice = price.unit_compare_amount

  return (
    <div className={cn("flex flex-col justify-end items-start",
      !!cx && cx,
    )}
    >
      <PriceCard
        price={displayPriceAmount}
        currency={displayPriceCurrency}
        comparePrice={displayComparePrice}
        isSubscription={isSubscription}
      />
    </div>
  )
}

export {
  SingleOptionComponent,
  MultiOptionComponent,
  PriceAndAddToCardComponent,
  PriceSelector,
  PriceDisplay
}