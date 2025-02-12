"use client";

import { createContext, useState } from "react";

type CartModalContext = {
  isOpen: boolean;
  open: () => void;
  close: () => void;
};

const CartModalContext = createContext<CartModalContext | null>({
  isOpen: false,
  open: () => { },
  close: () => { },
});

export const useCartModal = () => {
  const context = CartModalContext;

  if (!context) {
    throw new Error("useCartModal must be used within a <CartModalProvider />");
  }

  return context;
};

const CartModalProvider = ({ children }: { children: React.ReactNode }) => {
  const [isOpen, setIsOpen] = useState(false);

  const open = () => setIsOpen(true);
  const close = () => setIsOpen(false);

  return (
    <CartModalContext.Provider value={{ isOpen, open, close }}>
      {children}
    </CartModalContext.Provider>
  );
};

export default CartModalProvider;