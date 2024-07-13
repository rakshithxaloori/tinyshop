"use client";

import { createContext, useContext, useState } from "react";

// TODO: handle multiple option-variants
type VariantContext = {
  variant: any;
  setVariant: any;
}

const VariantContext = createContext<VariantContext | null>({
  variant: {
    prices: {},
  },
  setVariant: null,
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

  return (
    <VariantContext.Provider value={{ variant, setVariant }}>
      {children}
    </VariantContext.Provider>
  )
}

export default Variant