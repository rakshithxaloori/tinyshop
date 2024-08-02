import {
  CurrencyIconComponent,
  CurrencyString
} from "./currency-icon";

interface PriceCardProps {
  price: string | number;
  currency: string;
  comparePrice?: number | string;
  isSubscription?: boolean;
}

const PriceCard = (props: PriceCardProps) => {
  const {
    price,
    currency,
    comparePrice,
    isSubscription
  } = props;


  // Remove 2 zeros from the price from the end
  const displayPrice = (Number(price) / 100).toString()
  const displayComparePrice = (Number(comparePrice) / 100)?.toString()

  if (comparePrice) {
    return (
      <div className="flex items-center w-max-content gap-2">
        <span className="text-2xl font-bold flex flex-row items-center">
          <CurrencyIconComponent currency={currency} />
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
    <div className="flex items-center">
      <CurrencyIconComponent currency={currency} />
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

export default PriceCard