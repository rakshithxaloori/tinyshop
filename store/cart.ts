"use client";
import { TCartItem, TItemChain } from '@/types/cart';
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware'

export type TCartStore = {
  id: string;
  items: TCartItem[];
};

type TCartStoreReturnType = {
  quantity: number;
}

type TCartStoreGetters = {
  getProduct: (productId: string) => TCartStoreReturnType;
  getVariant: (variantId: string) => TCartStoreReturnType;
  getPrice: (priceId: string) => TCartStoreReturnType;
};

type TCartStoreActions = {
  addItem: (chain: TItemChain) => void;
  removeItem: (chain: TItemChain) => void;
  clearCartItem: (cartItemId: string) => void;
  clearCart: () => void;
} & TCartStoreGetters;

const useCartStore = create<TCartStore & TCartStoreActions>()(
  persist(
    (set, get) => ({
      id: '',
      items: [],
      // the setter functions
      addItem: (chain: TItemChain) => {
        const existingItem = get().items.find(i => i.priceId === chain.priceId);
        if (existingItem) {
          existingItem.quantity += 1;
          set({ items: [...get().items] });
        } else {
          set({ items: [...get().items, { ...chain, quantity: 1, id: Math.random().toString() }] });
        }
      },
      removeItem: (chain: TItemChain) => {
        const existingItem = get().items.find(i => i.priceId === chain.priceId);
        if (!existingItem) {
          return;
        }

        if (existingItem.quantity > 1) {
          existingItem.quantity -= 1;
        } else {
          set({ items: get().items.filter(i => i.priceId !== chain.priceId) });
        }
      },
      clearCartItem: (cartItemId: string) => {
        set({ items: get().items.filter(i => i.id !== cartItemId) });
      },
      clearCart: () => {
        set({ items: [] });
      },
      // the getter functions
      getProduct: (productId: string): TCartStoreReturnType => {
        // add the quantity of all items of the product which matches the productId
        const quantity = get().items.filter(i => i.productId === productId).reduce((acc, item) => acc + item.quantity, 0);
        return { quantity };
      },
      getVariant: (variantId: string): TCartStoreReturnType => {
        const quantity = get().items.filter(i => i.variantId === variantId).reduce((acc, item) => acc + item.quantity, 0);
        return { quantity };
      },
      getPrice: (priceId: string): TCartStoreReturnType => {
        const quantity = get().items.filter(i => i.priceId === priceId).reduce((acc, item) => acc + item.quantity, 0);
        return { quantity };
      },
      // End of setter and getter functions
    })
    ,
    {
      name: 'cart-storage',
      storage: createJSONStorage(() => localStorage),
    }
  ),
);

export default useCartStore;