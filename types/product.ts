type ProductConciseReview = {
  rating: number | null;
  count: number | null;
}

export type TPriceUI = {
  id: string;
  currency: string;
  unit_amount: number | null;
  unit_compare_amount: number | null;
}

export type TProductUICard = {
  id: string;
  handle: string;
  name: string;
  images: string[];
  default_variant: {
    id: string;
    prices: {
      data: TPriceUI[]
    }
  },
}
export type TProduct = TProductUICard

