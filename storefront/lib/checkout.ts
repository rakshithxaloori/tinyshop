"use server";

import { CheckoutCreate } from "@tinyshop/tinyshop-node/interfaces/checkout";
import { tinyshop } from "./tinyshop";
import { CustomerUpdate } from "@tinyshop/tinyshop-node/interfaces/customer";
import { CustomerAddressCreate } from "@tinyshop/tinyshop-node/interfaces/customerAddress";

export const createCheckout = async (cartId: string, customerId: string) => {
  "use server";
  const checkoutObject: CheckoutCreate = {
    cart: cartId,
    customer: customerId,
    return_url: "https://example.com/checkout/success",
    success_url: "https://example.com/checkout/success",
    url: "https://google.com/checkouts/{CHECKOUT_ID}"
  }
  const checkout = await tinyshop.checkouts.create(checkoutObject);
  return checkout;
}

export const deleteCheckout = async (checkoutId: string) => {
  "use server";
  const checkout = await tinyshop.checkouts.delete(checkoutId);
  return checkout;
}

export const updateCheckout = async (checkoutId: string,
  customerAddress: string) => {
  "use server";
  const checkout = await tinyshop.checkouts.update(checkoutId, { customer_address: customerAddress });
  return checkout;
}

export const updateCustomerDetails = async (
  customerId: string,
  details: CustomerUpdate
) => {
  "use server";
  const updatedCustomer = await tinyshop.customers.update(customerId, details);
  return updatedCustomer
}

export const createCustomerAddress = async (
  customerAddressDetails: CustomerAddressCreate
) => {
  "use server";
  const customerAddress = await tinyshop.customerAddresses.create(customerAddressDetails);
  return customerAddress;
}