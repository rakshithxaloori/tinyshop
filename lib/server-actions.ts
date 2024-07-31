"use server";

import { getSessionData } from "./session";

export const checkIfAuthenticated = async () => {
  "use server";
  const data = await getSessionData()
  return !!data?.customerId
}