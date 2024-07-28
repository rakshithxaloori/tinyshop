type ProductConciseReview = {
  rating: number | null;
  count: number | null;
}

export type TPriceUI = {
  type: string;
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
    name: string;
    id: string;
    prices: {
      data: TPriceUI[]
    }
  },
}
export type TProduct = TProductUICard

export type TProductFAQ = {
  question: string;
  answer: string;
}

export type TProductFAQSection = {
  title: string;
  data: TProductFAQ[];
}

export type TProductTabs = {
  title: string;
  content: {
    text: string;
    image: {
      src: string;
      alt: string;
    }
  }
}

export interface IProductExternalDetails {
  brand: string;
  product_handle: string;
  faq: TProductFAQSection | null;
  tabs: {
    data: TProductTabs[];
  }
}

