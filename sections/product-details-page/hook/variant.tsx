"use client";

import { createContext, useContext, useState } from "react";

// TODO: handle multiple option-variants
type VariantContext = {
  price: any;
  setPrice: any;
}

const VariantContext = createContext<VariantContext | null>({
  price: {
    id: "",
    currency: "",
    unit_amount: 0,
    unit_compare_amount: 0,
    type: "",
  },
  setPrice: null
})

export const useVariant = () => {
  const context = useContext(VariantContext)

  if (!context) {
    throw new Error("useVariant must be used within a <Variant />")
  }

  return context
}

const Variant = ({ children }: { children: React.ReactNode }) => {
  const [price, setPrice] = useState({
    id: "",
    currency: "",
    unit_amount: 0,
    unit_compare_amount: 0,
    type: "",
  })

  return (
    <VariantContext.Provider value={{ price, setPrice }}>
      {children}
    </VariantContext.Provider>
  )
}

export default Variant