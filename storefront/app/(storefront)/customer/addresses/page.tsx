"use server";

import CustomerAddressPage from "@/components/pages/customer-portal/address";
import { getSessionData } from "@/lib/session";
import { getCustomerAddresses } from "@/lib/storefront";
import { Suspense } from "react";

export default async function AddressesPage() {
  const session = await getSessionData();
  if (!session) {
    return null;
  }

  const { customerId } = session;
  const addresses = await getCustomerAddresses(customerId);


  return (
    <Suspense fallback={<div>Loading...</div>}>
      <CustomerAddressPage customerAddressList={addresses} />
    </Suspense>
  )
}