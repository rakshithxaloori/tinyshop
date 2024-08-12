import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

import Image from "next/image";
import { cn } from "@/lib/utils";
import { LayoutClasses as TProductLayoutClass } from "@/types/layout";

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

  return (
    <Card className={cn(`w-full h-fit max-w-sm mx-auto bg-blue-100`, layout.containerClass)}>
      <div className={cn("relative h-24 w-24", layout.imageClass)}>
        <Image
          src={images[0] || '/api/placeholder/400/400'}
          alt={name}
          width={96}
          height={96}
          className="aspect-square rounded-lg"
        />
      </div>
      <div className={layout.contentClass}>
        <h2 className={layout.titleClass}>{name}</h2>
        <p className={layout.variantClass}>{default_variant.name}</p>
        <div className={layout.priceClass}>
          <span>{formatPrice(price.unit_amount)}</span>
          {price.unit_compare_amount && (
            <span className={layout.compareAtPriceClass}>
              {formatPrice(price.unit_compare_amount)}
            </span>
          )}
        </div>
        <Badge className={layout.badgeClass} variant="secondary">{price.type}</Badge>
      </div>
    </Card>
  );
}

export default ProductCard;