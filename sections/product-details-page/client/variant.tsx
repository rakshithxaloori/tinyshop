"use client";

import PriceCard from "@/components/price/price-card-v1";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { MinusIcon, PlusIcon, ShoppingBagIcon } from "lucide-react";
import { Fragment, use, useEffect, useMemo, useRef, useState } from "react";
import { useVariant } from "../hook/variant";
import useCartStore from "@/store/cart";
import dynamic from "next/dynamic";
import { TPriceUI } from "@/types/product";
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { px } from "framer-motion";

const processPricesResponse = (prices: any): TPriceUI[] => {
  // Prices are returned as an array of objects
  // return the currency, the unit_amount and the unit_compare_amount
  // if available
  return prices.map((price: any) => {
    const { currency,
      unit_amount,
      unit_compare_amount,
      id,
      type,
    } = price;
    return {
      type,
      id,
      currency,
      unit_amount,
      unit_compare_amount
    }
  });
}


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
  const { variant: selectedVariant, price: selectedPrice } = useVariant();
  const { shouldAnimateButton } = config
  const { items, addItem } = useCartStore()

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
    variantId: selectedVariant?.id || "",
    priceId: selectedPrice?.id || "",
  }

  const cartItemDisplay = {
    image: product.images.length ? product.images[0] : "",
    name: product.name,
    variantName: selectedVariant?.name || "",
    price: selectedPrice?.unit_amount || 0,
    currency: selectedPrice?.currency || "",
    isSubscription: selectedPrice?.type === "subscription",
  }

  const handleAddToCart = (e: any) => {
    e.preventDefault();
    e.stopPropagation();
    addItem(cartItemChain, cartItemDisplay, quantity)
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

const VariantItem = ({ variant, selectedVariant, onSelect, onPriceSelect }: {
  variant: any; selectedVariant: any;
  onSelect: Function;
  onPriceSelect: Function;
}) => {
  // display the one_time of the variant
  const { prices } = variant;
  const uiPrices = processPricesResponse(prices.data)
  const hasSubscription = uiPrices.some(price => price.type === "subscription")
  const isSelected = useMemo(() => selectedVariant.id === variant.id, [selectedVariant, variant])

  return (
    <div className={cn("flex flex-row min-w-full item-center h-full p-2 mt-2",
      isSelected ? "border-2 border-primary" : "border-2 border-primary",
      isSelected ? "border-opacity-100" : "border-opacity-0",
      "hover:border-primary hover:border-opacity-100 cursor-pointer transition-all",
      // isSelected && "cursor-not-allowed",
    )}
      onClick={() => onSelect(variant)}
    >
      {
        hasSubscription ? (
          <SubscriptionVariantDisplay variant={variant} isSelected={isSelected}
            onPriceSelect={onPriceSelect} />
        ) : (
          <SansSubcriptionVariantDisplay variant={variant} />
        )
      }
    </div>
  )
}

const SubscriptionVariantDisplay = ({ variant, isSelected, onPriceSelect }: { variant: any; isSelected: boolean; onPriceSelect: Function }) => {
  const { prices } = variant;
  const uiPrices = useMemo(() => processPricesResponse(prices.data), [prices])
  const { getPrice } = useCartStore()
  const { price: selectedPrice } = useVariant()
  const cartPriceQty = uiPrices.map((price: any) => getPrice(price.id).quantity)

  const [pxValue, setPxValue] = useState<string>(prices.data[0].id)

  useEffect(() => {
    if (!isSelected) {
      setPxValue("")
    } else {
      setPxValue(uiPrices[0].id)
    }
  }, [isSelected, uiPrices])

  useEffect(() => {
    if (isSelected) {
      const uEPrice = uiPrices.find(price => price.id === pxValue)
      onPriceSelect(uEPrice)
    }
  }, [isSelected, pxValue, uiPrices, onPriceSelect])


  const onValueChange = (priceId: string) => {
    setPxValue(priceId)

    // const selectedPrice = uiPrices.find(price => price.id === priceId)
    // onPriceSelect(selectedPrice)
  }

  return (
    <div className="flex flex-row flex-1">
      <span className="text-lg font-bold">{variant.name}</span>
      <div className="grow"></div>
      <div className="flex flex-col mt-sm gap-2">
        <RadioGroup value={pxValue} disabled={!isSelected}
          onValueChange={(value: string) => onValueChange(value)}
        >
          {
            uiPrices.map((price: any, index: number) => {
              return (
                <div key={index} className="flex items-center space-x-2 w-full">
                  <RadioGroupItem
                    value={price.id}
                    id={price.id}
                  />
                  <Label htmlFor={price.id} className="flex flex-row items-center w-full justify-between">
                    <PriceCard price={price.unit_amount} currency={price.currency}
                      isSubscription={price.type === "subscription"}
                    />
                    <NoSSRCartBagDisplay quantity={cartPriceQty[index]} cx="ml-2" />
                  </Label>
                </div>
              )
            }
            )
          }
        </RadioGroup>
      </div>
    </div>
  )
}

const SansSubcriptionVariantDisplay = ({ variant }: { variant: any }) => {
  const { prices } = variant;
  const priceAmount = prices.data[0].unit_amount
  const priceCurrency = prices.data[0].currency
  const { getVariant } = useCartStore()
  const cartVariantQty = getVariant(variant.id).quantity
  return (
    <div className="flex flex-row flex-1">
      <span className="text-lg font-bold">{variant.name}</span>
      <div className="grow"></div>
      <PriceCard price={priceAmount} currency={priceCurrency} />
      <NoSSRCartBagDisplay quantity={cartVariantQty} cx="ml-2" />
    </div>
  )

}


const VariantSelector = ({ product }: { product: any }) => {
  const variantInfo = product.variants.data
  const [selectedVariant, setSelectedVariant] = useState(variantInfo[0])
  const { setVariant, setPrice } = useVariant();
  const { getProduct } = useCartStore()
  const cartProductQty = getProduct(product.id).quantity

  useEffect(() => {
    setVariant(selectedVariant)
  }, [setVariant, selectedVariant])

  const handleSelectVariant = (localVariant: any) => {
    setSelectedVariant(localVariant)
    // if the local variant has a single price then set it to the price
    // const { prices } = localVariant;
    // const uiPrices = processPricesResponse(prices.data)
    // const selectedPrice = uiPrices.find(price => price.type === "one_time")
    // setPrice(selectedPrice)
  }

  const handleSelectPrice = (price: any) => {
    setPrice(price)
  }

  return (
    <div className={cn("flex flex-col w-full overflow-x-scroll mt-md",
      (variantInfo.length === 1 && cartProductQty === 0) && "hidden"
    )}>
      {
        variantInfo.map((variant: any, index: number) => {
          return (
            <VariantItem
              key={index}
              {...{ variant, selectedVariant, }}
              onSelect={handleSelectVariant}
              onPriceSelect={handleSelectPrice}
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
  const { variant, price } = useVariant()
  if (!variant) {
    return null
  }
  const { prices } = variant;
  // check if it's a subscription variant
  const hasSubscription = prices.data.some((price: any) => price.type === "subscription")
  let displayPriceAmount = prices.data[0].unit_amount
  const displayPriceCurrency = prices.data[0].currency
  const displayComparePrice = prices.data[0].unit_compare_amount

  return (
    <div className={cn("flex flex-col justify-end items-start",
      !!cx && cx,
    )}
    >
      {!hasSubscription &&
        (<PriceCard
          price={displayPriceAmount}
          currency={displayPriceCurrency}
          comparePrice={displayComparePrice}
        />)
      }
      {
        hasSubscription && (
          (
            <Fragment>
              <div className="flex flex-row items-center gap-1 md:gap-2">
                <span className="text-sm font-bold">{"Buy    "} @ </span>

                <PriceCard
                  price={prices.data[0].unit_amount}
                  currency={prices.data[0].currency}
                  comparePrice={prices.data[0].unit_compare_amount}
                />
              </div>
              <div className="flex flex-row items-center gap-1 md:gap-2">
                <span className="text-sm font-bold">Subscribe @ </span>
                <PriceCard
                  price={prices.data[1].unit_amount}
                  currency={prices.data[1].currency}
                  comparePrice={prices.data[1].unit_compare_amount}
                  isSubscription
                />
              </div>
            </Fragment>
          )
        )
      }
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