
import { cn } from "@/lib/utils";
import Image from "next/image";

interface ProductVariantSectionProps {
  product: any;
  fallbackOptions?: any;
  reviews: any[];
}

import {
  PriceAndAddToCardComponent,
  PriceDisplay,
  VariantSelector
} from "./client/variant";
import Variant from "./hook/variant";
import Link from "next/link";

const ProductImage = ({
  product,
  fallbackImage }: { product: any, fallbackImage: string }) => {
  let imageArray = product.images ?? [
    fallbackImage
  ]
  return (
    <div className="flex flex-col w-full aspect-square h-fit justify-center md:sticky md:top-[10rem]">
      <div className="carousel flex-1 rounded-box w-full">
        {
          imageArray.map((image: string, index: number) => {
            const imageId = "product-image-" + index
            return (
              <div key={index} id={imageId} className="carousel-item relative min-h-full min-w-full border-primary gap-1">
                <Image
                  src={image}
                  alt={product.name}
                  fill
                  className="rounded"
                />
              </div>
            )
          })
        }
      </div>

    </div>
  )
}

const htmlToText = (htmlString: string) => {
  return htmlString.replace(/<\/?[^>]+(>|$)/g, "");
};

const ProductDetails = ({ product, reviews }: { product: any; reviews: any[] }) => {
  const summary = product.description ? htmlToText(product.description) : "";
  // compute avg rating
  const numReviews = reviews.length;
  const avgRating = numReviews === 0 ? 0 : reviews.reduce((acc, review) => acc + review.product_rating, 0) / numReviews;
  const displayRating = avgRating.toFixed(1)
  return (
    <div className="flex flex-col w-full h-full p-2 max-sm:mt-sm p-2">
      <h1 className="text-3xl font-bold">{product.name}</h1>
      <div className="flex items-center mt-sm">
        <div className="flex items-center gap-1">
          <span className="text-lg font-bold">{displayRating}</span>
          <div className="flex items-center">
            <svg className="w-4 h-4 fill-current text-warning" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M10 0l2.6 6.3L20 7.2l-5.2 4.5 1.6 6.2L10 15.4 3.6 18l1.6-6.2L0 7.2l7.4-.9L10 0z" />
            </svg>
          </div>
        </div>
        <div className="ml-sm text-sm font-semibold">{"| "}</div>
        <Link href="#pdp-reviews-section">
          <div className="link ml-sm text-sm font-semibold">{numReviews} reviews</div>
        </Link>
      </div>
      <PriceDisplay cx="mt-lg" />
      <div className="mt-md line-clamp-4">
        {summary}
      </div>
      <div className="grow" />
      <VariantSelector product={product} />
      <PriceAndAddToCardComponent product={product} />
    </div>
  )
}

const ProductVariantSection = ({ product, fallbackOptions, reviews }: ProductVariantSectionProps) => {
  return (
    <div className="flex flex-1 min-h-[40rem] w-full rounded mt-lg">
      <div className="grid grid-cols-1 md:grid-cols-2 md:grid-rows-1 gap-4 w-full min-h-full">
        <ProductImage product={product} fallbackImage={fallbackOptions?.fallbackImage} />
        <Variant>
          <ProductDetails product={product} reviews={reviews} />
        </Variant>
      </div>
    </div >
  )
}

export default ProductVariantSection