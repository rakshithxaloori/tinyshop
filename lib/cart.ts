"use server";

import { tinyshop } from "./tinyshop";

export const createCart = async () => {
  "use server";
  const cart = await tinyshop.carts.create({ "currency": "INR" })
  return cart;
}

export const deleteCart = async (cartId: string) => {
  "use server"
  const response = await tinyshop.carts.delete(cartId);
  return response
}

export const addCartItem = async (cartId: string, priceId: string, quantity: number) => {
  "use server";
  const cartItem = await tinyshop.cartItems.create({ cart: cartId, price: priceId, quantity });
  return cartItem;
}

export const removeCartItem = async (cartItemId: string) => {
  "use server"
  const response = await tinyshop.cartItems.delete(cartItemId);
  return response;
}

export const updateCartItem = async (cartItem: string, quantity: number) => {
  "use server"
  const response = await tinyshop.cartItems.update(cartItem, { quantity });
  return response;
}


