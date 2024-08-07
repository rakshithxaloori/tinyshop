import CustomerPortalHomePage from "@/components/pages/customer-portal/home"
import PhoneAuth from "@/components/phone-auth"
import { getSessionData } from "@/lib/session"

const CustomerPortalDisplayPage = async () => {
  const session = await getSessionData()
  if (!session) {
    return <PhoneAuth />
  }
  const { customerId } = session

  return <CustomerPortalHomePage customerId={customerId} />

}

export default CustomerPortalDisplayPage