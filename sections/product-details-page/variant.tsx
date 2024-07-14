
import { cn } from "@/lib/utils";
import Image from "next/image";

interface ProductVariantSectionProps {
  product: any;
  fallbackOptions?: any
}

import {
  PriceAndAddToCardComponent,
  PriceDisplay,
  VariantSelector
} from "./client/variant";
import Variant from "./hook/variant";

const ProductImage = ({
  product,
  fallbackImage }: { product: any, fallbackImage: string }) => {
  let imageArray = product.images ?? [
    fallbackImage
  ]
  return (
    <div className="flex flex-col w-full h-full justify-center">
      <div className="carousel flex-1 rounded-box w-full">
        {
          imageArray.map((image: string, index: number) => {
            const imageId = "product-image-" + index
            return (
              <div key={index} id={imageId} className="carousel-item relative min-h-full min-w-full border-primary gap-1">
                <Image
                  src={image}
                  alt={product.name}
                  layout="fill"
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


const ProductDetails = ({ product }: { product: any }) => {
  const randomText = "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cumque odit doloribus voluptate dolorum numquam quos dolores a quisquam culpa, et rem reprehenderit placeat odio fugiat ab iure corrupti! Doloribus, et?"
  const summary = product.summary || randomText
  return (
    <div className="flex flex-col w-full h-full p-2">
      <h1 className="text-3xl font-bold">{product.name}</h1>
      <PriceDisplay cx="mt-lg" />
      <div className="mt-md">
        {summary}
      </div>
      <div className="grow" />
      <VariantSelector product={product} />
      <PriceAndAddToCardComponent product={product} />
    </div>
  )
}

const ProductVariantSection = ({ product, fallbackOptions }: ProductVariantSectionProps) => {
  return (
    <div className="flex flex-1 min-h-[40rem] max-h-[85vh] w-full rounded mt-lg">
      <div className="grid grid-cols-1 md:grid-cols-2 grid-rows-2 md:grid-rows-1 gap-4 w-full min-h-full">
        <ProductImage product={product} fallbackImage={fallbackOptions?.fallbackImage} />
        <Variant>
          <ProductDetails product={product} />
        </Variant>
      </div>
    </div >
  )

}

export default ProductVariantSection