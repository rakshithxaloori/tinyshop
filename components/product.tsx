import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

import Image from "next/image";
import { cn } from "@/lib/utils";
import { EmotionLayoutStyles as TProductLayoutClass } from "@/types/layout";
import { tailwindToEmotionCSS } from "@/lib/tailwind";
import { twMerge } from "tailwind-merge";
import { twj } from "tw-to-css";
import { css } from "@emotion/css";

export type TPriceUI = {
  type: string;
  id: string;
  currency: string;
  unit_amount: number | null;
  unit_compare_amount: number | null;
}

type TProductCardData = {
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
};

interface ProductCardProps {
  data: TProductCardData;
  layout: TProductLayoutClass;
}

const ProductCard: React.FC<ProductCardProps> = ({ data, layout }) => {
  const { name, images, default_variant } = data;
  const price = default_variant.prices.data[0];

  const formatPrice = (amount: number | null) => {
    if (amount === null) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: price.currency,
    }).format(amount / 100); // Assuming the amount is in cents
  };

  console.log(layout);
  console.log(layout.container);

  return (
    <Card className={
      cn(
        css`
      ${(layout.container)};
      `,
        "h-fit w-full max-w-md"
      )

    }
    >
      <div className={cn("relative",
        css`
        ${(layout.image)};
        `
      )}
      >
        <Image
          src={images[0] || '/api/placeholder/400/400'}
          alt={name}
          fill
          className="rounded-lg"
        />
      </div>
      <div
        className={cn(
          css`
          ${(layout.content)};`
        )}
      >
        <h2 className={css`${(layout.title)};`}>{name}</h2>
        <p className={css`${(layout.variant)};`}>{default_variant.name}</p>
        <div
          className={css`${(layout.price)};`}
        >
          <span>{formatPrice(price.unit_amount)}</span>
          {price.unit_compare_amount && (
            <span
              className={css`${(layout.compareAtPrice)};`}>
              {formatPrice(price.unit_compare_amount)}
            </span>
          )}
        </div>
        <Badge
          className={css`${(layout.badge)};`}
          variant="secondary">{price.type}</Badge>
      </div>
    </Card>
  );
}

export default ProductCard;