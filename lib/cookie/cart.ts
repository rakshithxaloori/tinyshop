"use server";

import { cookies } from 'next/headers'
import { createCart } from '../cart';

const cartCookieName = 'cart'

const initCartId = async () => {
  const cookieStore = cookies()
  // check if cart cookie exists
  const cartCookie = cookieStore.get(cartCookieName)

  if (!cartCookie || !cartCookie.value) {
    // create a new cart
    const cart = await createCart()
    try {
      cookieStore.set(cartCookieName, cart.id, {
        maxAge: 60 * 60 * 24 * 14 // 2 weeks
      })
    } catch (error) {
      console.error('Error setting cart cookie:', error)
    }
    return cart.id
  } else {
    return cartCookie.value
  }
}

export const getCartId = async () => {
  const cookieStore = cookies()
  const cartCookie = cookieStore.get(cartCookieName)
  let cartId: string;
  if (!cartCookie || !cartCookie.value) {
    cartId = await initCartId()
  } else {
    cartId = cartCookie.value
  }
  return cartId;
}