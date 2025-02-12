
import CheckoutCartDisplay from "../checkout-cart-display";
import CheckoutForm from "../checkout-form";
import { CustomerSession } from "@/types/session";
import PhoneAuth from "../phone-auth";

interface CheckoutPageProps {
  session: CustomerSession | null
}


const CheckoutPage = (props: CheckoutPageProps) => {
  const { session } = props
  const auth = !!session?.customerId;
  return (
    <div className="grid lg:grid-cols-1 lg:grid-cols-12 lg:gap-x-8 w-fit">
      <CheckoutCartDisplay />
      {auth ? (<CheckoutForm {...{ session }} className="lg:col-span-5" />) : (
        <PhoneAuth className="lg:col-span-5" />
      )}
    </div>
  )
}

export default CheckoutPage