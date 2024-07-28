"use client";

import { createContext, useContext, useState } from "react";

// TODO: handle multiple option-variants
type VariantContext = {
  variant: any;
  price: any;
  setVariant: any;
  setPrice: any;
}

const VariantContext = createContext<VariantContext | null>({
  variant: {
    prices: {},
  },
  price: null,
  setVariant: null,
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
  const [variant, setVariant] = useState(null)
  const [price, setPrice] = useState(null)

  return (
    <VariantContext.Provider value={{ variant, setVariant, price, setPrice }}>
      {children}
    </VariantContext.Provider>
  )
}

export default Variant