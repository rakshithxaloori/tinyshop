type TItemChain = {
  priceId: string;
  variantId: string;
  productId: string;
}

type TCartItem = {
  id: string;
  quantity: number;
} & TItemChain;

export type {
  TItemChain,
  TCartItem
}