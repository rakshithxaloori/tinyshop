import { CoinsIcon, DollarSignIcon, EuroIcon, IndianRupeeIcon, JapaneseYenIcon, PoundSterlingIcon, RussianRubleIcon, SwissFrancIcon } from "lucide-react"

const CurrencyIconComponent = ({ currency }: { currency: string }) => {
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

export {
  CurrencyIconComponent,
  CurrencyString
}