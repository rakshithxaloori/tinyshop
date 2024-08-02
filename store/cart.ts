"use client";
import { TCartItem, TCartItemDisplay, TItemChain } from '@/types/cart';
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware'
import { getCartId } from '@/lib/cookie/cart';
import { addCartItem, deleteCart, removeCartItem, updateCartItem } from '@/lib/cart';

export type TCartStore = {
  id: string;
  items: TCartItem[];
};

type TCartStoreReturnType = {
  quantity: number;
}

type TCartStoreGetters = {
  getId: () => string;
  getProduct: (productId: string) => TCartStoreReturnType;
  getVariant: (variantId: string) => TCartStoreReturnType;
  getPrice: (priceId: string) => TCartStoreReturnType;
};

type TCartRehydrateActions = {
  rehydrate: () => Promise<string>;
}

type TCartStoreActions = {
  setId: (id: string) => void;
  addItem: (chain: TItemChain, display: TCartItemDisplay, quantity: number) => void;
  removeItem: (chain: TItemChain) => void;
  clearCartItem: (cartItemId: string) => void;
  clearCart: () => void;
} & TCartStoreGetters & TCartRehydrateActions;

const useCartStore = create<TCartStore & TCartStoreActions>()(
  persist(
    (set, get) => ({
      id: '',
      setId: (id: string) => set({ id }),
      getId: () => get().id,
      items: [],
      // the setter functions
      addItem: async (chain: TItemChain, display: TCartItemDisplay, quantity: number = 1) => {
        // await the rehydrate function
        const cartId = await get().rehydrate();
        const existingItem = get().items.find(i => i.priceId === chain.priceId);
        if (existingItem) {
          existingItem.quantity += quantity;
          const updateItem = await updateCartItem(existingItem.id, existingItem.quantity);
          set({ items: [...get().items] });
        } else {
          const { id: cartItemId } = await addCartItem(cartId, chain.priceId, quantity);
          set({
            items: [...get().items, {
              ...chain,
              quantity: quantity,
              id: cartItemId,
              ...display

            }]
          });
        }
      },
      removeItem: async (chain: TItemChain) => {
        const cartId = await get().rehydrate();
        const existingItem = get().items.find(i => i.priceId === chain.priceId);
        if (!existingItem) {
          return;
        }
        if (existingItem.quantity > 1) {
          existingItem.quantity -= 1;
          const updateItem = await updateCartItem(existingItem.id, existingItem.quantity);
          set({ items: [...get().items] });
        } else {
          const removeItem = await removeCartItem(existingItem.id);
          set({ items: get().items.filter(i => i.priceId !== chain.priceId) });
        }
      },
      clearCartItem: async (cartItemId: string) => {
        const cartId = await get().rehydrate();
        const removeItem = await removeCartItem(cartItemId);
        set({ items: get().items.filter(i => i.id !== cartItemId) });
      },
      clearCart: async () => {
        const cartId = await get().rehydrate();
        for (const item of get().items) {
          get().clearCartItem(item.id);
        }
        set({ items: [] });
      },

      // the getter functions. DO NOT rehydrate here
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

      // rehydrate function
      rehydrate: async () => {
        const cartId = await getCartId();
        const zustandCartId = get().id;
        if (zustandCartId !== cartId && zustandCartId.length > 0) {
          // delete the previous cart 
          await deleteCart(zustandCartId);
          // TODO: rehydrate the cart items
        }
        set({ id: cartId });
        return cartId;
      }
    })
    ,
    {
      name: 'cart-storage',
      storage: createJSONStorage(() => localStorage),
      // ideally we should create a async storage with rehydrate technique
    }
  ),
);

export default useCartStore;