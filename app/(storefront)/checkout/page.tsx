import CheckoutPage from "@/components/pages/checkout-page"
import { checkIfAuthenticated } from "@/lib/server-actions"
import { getSessionData } from "@/lib/session"

const CheckoutDisplayPage = async () => {
  const sessionData = await getSessionData()
  return (
    <CheckoutPage session={sessionData} />
  )
}

export default CheckoutDisplayPage