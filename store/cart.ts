import { create } from 'zustand';
import { cookies } from 'next/headers';

export type IAddToCart = (domain: string, variant_id: string) => Promise<void>;

export type IRemoveFromCart = (
  domain: string,
  variant_id: string,
  is_remove: boolean
) => Promise<void>;

export type TCartCookie = {
  [variant_id: string]: number;
};

export type TCart = {
  [domain: string]: TCartCookie;
};

export type TCartStore = {
  cart: TCart;
  addToCart: IAddToCart;
  removeFromCart: IRemoveFromCart;
};

const useCartStore = create<TCartStore>((set) => ({
  cart: {},
  addToCart: async (domain, variant_id) => {
    set((state) => {
      const cart = state.cart;
      if (cart[domain]) {
        if (cart[domain][variant_id]) {
          cart[domain][variant_id] += 1;
        } else {
          cart[domain][variant_id] = 1;
        }
      } else {
        cart[domain] = {
          [variant_id]: 1,
        };
      }
      return { cart };
    });
  },
  removeFromCart: async (domain, variant_id, is_remove) => {
    set((state) => {
      const cart = state.cart;
      if (cart[domain]) {
        if (cart[domain][variant_id]) {
          if (is_remove) {
            delete cart[domain][variant_id];
          } else {
            cart[domain][variant_id] -= 1;
          }

          if (cart[domain][variant_id] === 0) {
            delete cart[domain][variant_id];
          }

          if (Object.keys(cart[domain]).length === 0) {
            delete cart[domain];
          }
        }
      }
      return { cart };
    });
  },
}));

export default useCartStore;