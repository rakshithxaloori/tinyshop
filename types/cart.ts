type TItemChain = {
  priceId: string;
  variantId: string;
  productId: string;
}

type TCartItemDisplay = {
  image: string;
  price: number | string;
  name: string;
  currency: string;
}

type TCartItem = {
  id: string;
  quantity: number;
} & TItemChain & TCartItemDisplay

export type {
  TItemChain,
  TCartItem,
  TCartItemDisplay
}