"use server";

import { cookies } from "next/headers"

const getCartId = async () => {
  const cart = cookies().get('cart');
  if (!cart) {
    return null;
  } else {
    const cartValue = cart.value;
    const tCart = JSON.parse(cartValue) as string;
    return tCart;
  }
}

const setCartCookie = (cart: any) => {
  cookies().set('cart', JSON.stringify(cart));
}

export { getCartId, setCartCookie };
