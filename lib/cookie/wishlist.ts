"use server";

import { cookies } from 'next/headers'

const wishlistCookieName = 'wishlist'

export const getWishlist = (): Promise<string[]> => {
  const cookieStore = cookies()
  const cookie = cookieStore.get(wishlistCookieName)

  if (!cookie || !cookie.value) {
    return Promise.resolve([])
  }

  const wishlist = JSON.parse(cookie.value) as string[]
  return Promise.resolve(wishlist)
}

export const setWishlist = async (wishlist: string[]) => {
  const cookieStore = cookies()

  try {
    cookieStore.set(wishlistCookieName, JSON.stringify(wishlist), {
      maxAge: 60 * 60 * 24 * 365 // 1 year
    })
  } catch (error) {
    console.error('Error setting wishlist cookie:', error)
  }
}

export const addToWishlist = async (productId: string) => {
  const wishlist = await getWishlist()

  if (!wishlist.includes(productId)) {
    wishlist.push(productId)
    setWishlist(wishlist)
  }
}

export const removeFromWishlist = async (productId: string) => {
  const wishlist = await getWishlist()
  const index = wishlist.indexOf(productId)

  if (index > -1) {
    wishlist.splice(index, 1)
    setWishlist(wishlist)
  }
}

export const hasWishlistItem = async (productId: string) => {
  const wishlist = await getWishlist()
  return wishlist.includes(productId)
}

export const clearWishlist = async () => {
  setWishlist([])
}