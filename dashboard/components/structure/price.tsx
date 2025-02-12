import { cn } from "@/lib/utils"
import { CoinsIcon, DollarSignIcon, EuroIcon, IndianRupeeIcon, JapaneseYenIcon, PoundSterlingIcon, RussianRubleIcon, SwissFrancIcon } from "lucide-react"

const CurrencyIcon = ({ currency }: { currency: string }) => {
  currency = currency.toLowerCase()
  if (currency === "usd") {
    return <DollarSignIcon />
  } else if (currency === "inr") {
    return <IndianRupeeIcon />
  } else if (currency === "eur") {
    return <EuroIcon />
  } else if (currency === "gbp") {
    return <PoundSterlingIcon />
  } else if (currency === "yen") {
    return <JapaneseYenIcon />
  } else if (currency === "rub") {
    return <RussianRubleIcon />
  } else if (currency === "swiss") {
    return <SwissFrancIcon />
  } else {
    return <CoinsIcon />
  }
}

const CurrencyString = ({ currency }: { currency: string }) => {
  currency = currency.toLowerCase()
  if (currency === "usd") {
    return "$"
  } else if (currency === "inr") {
    return "₹"
  } else if (currency === "eur") {
    return "€"
  } else if (currency === "gbp") {
    return "£"
  } else if (currency === "yen") {
    return "¥"
  } else if (currency === "rub") {
    return "₽"
  } else if (currency === "swiss") {
    return "₣"
  } else {
    return "¢"
  }
}

interface PriceStructureProps {
  price: string | number;
  currency: string;
  comparePrice?: number | string;
  isSubscription?: boolean;
  className?: string;
}

const PriceStructure = (props: PriceStructureProps) => {
  const {
    price,
    currency,
    comparePrice,
    isSubscription,
    className
  } = props;


  // Remove 2 zeros from the price from the end
  const displayPrice = (Number(price) / 100).toString()
  const displayComparePrice = (Number(comparePrice) / 100)?.toString()

  if (comparePrice) {
    return (
      <div className={cn("flex items-center w-max-content gap-2", className)}>
        <span className="text-2xl font-bold flex flex-row items-center text-base-content">
          <CurrencyIcon currency={currency} />
          {displayPrice}
        </span>
        <span className="text-2xl line-through text-base-content/60">
          <CurrencyString currency={currency} />
          {displayComparePrice}
        </span>
      </div >
    )
  }

  return (
    <div className={cn("flex items-center text-base-content", className)}>
      <CurrencyIcon currency={currency} />
      <span className="text-2xl font-bold">
        {displayPrice}
      </span>
      {isSubscription && (
        <span className="text-sm font-normal text-base-content/60 self-align-end">
          /mo
        </span>
      )}
    </div >
  )
}

export default PriceStructure;
