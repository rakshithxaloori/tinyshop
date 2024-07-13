"use client";
import { Cart, TCart } from '@/lib/cart';
import { create } from 'zustand';

export type TCartStore = {
  cart: TCart;
};

const getCartKey = (domain: string) => `cart-${domain}`;

const persistCart = (cart: TCart) => {

}

const useCartStore = create<TCartStore>((set, get) => ({
  cart: new Cart(),
}));

export default useCartStore;