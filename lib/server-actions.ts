"use server";

import { clearSessionData, getSessionData, setSessionData } from "./session";
import { createOrGetCustomer, verifyCustomer } from "./storefront";

export const checkIfAuthenticated = async () => {
  "use server";
  const data = await getSessionData()
  return !!data?.customerId
}

export const sendCustomerOtp = async (phoneNumber: string) => {
  "use server";
  const response = await createOrGetCustomer(phoneNumber)
  return response
}

export const verifyCustomerOtp = async (customerId: string, otp: string) => {
  "use server"
  const response = await verifyCustomer(customerId, otp)
  return response
}

export const logoutCustomer = async () => {
  "use server";
  clearSessionData()
}

export const signInCustomer = async (customerId: string, phoneNumber: string) => {
  "use server"
  await setSessionData(customerId, phoneNumber)
}