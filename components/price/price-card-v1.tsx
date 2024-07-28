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

  if (comparePrice) {
    return (
      <div className="flex items-center w-max-content gap-2">
        <span className="text-2xl font-bold flex flex-row items-center">
          <CurrencyIconComponent currency={currency} />
          {price}
        </span>
        <span className="text-2xl line-through text-base-content/60">
          <CurrencyString currency={currency} />
          {comparePrice}
        </span>
      </div >
    )
  }

  return (
    <div className="flex items-center">
      <CurrencyIconComponent currency={currency} />
      <span className="text-2xl font-bold">
        {price}
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