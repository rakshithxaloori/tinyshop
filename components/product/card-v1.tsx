
// The product card component consists of
// 1. product image
// 2. product name
// 3. product price
// 4. product discount
// 5. product rating
// 6. Cart actions
// 7. Wishlist actions
"use client";

import Image from "next/image";
import { GemIcon, SparkleIcon, HeartIcon, ShoppingCartIcon, ArrowUp, ArrowUpRightIcon } from "lucide-react";
import { Button } from "../ui/button";
import PriceCard from "@/components/price/price-card-v1";
import { processPricesResponse } from "@/lib/storefront";
import { useRouter } from "next/navigation";

const ProductCard = ({ product,
  fallbackOptions
}: {
  product: any;
  fallbackOptions: any;
}) => {
  const { image } = fallbackOptions;
  const productImage = product?.images && product.images[0] ? product.images[0] : image;
  const prices = product?.default_variant?.prices ? processPricesResponse(product?.default_variant?.prices?.data) : [];
  const router = useRouter();
  const handleAddToCart: React.MouseEventHandler<HTMLButtonElement> = (event) => {
    event.preventDefault();
    event.stopPropagation();

  };

  const handleLinkClick = () => {
    router.push(`/products/${product.handle}`);
  };

  return (
    <div onClick={handleLinkClick}
      className="card-wrapper cursor-pointer border-primary/60 hover:border-primary transition-colors duration-100	ease-linear border-2 rounded-xl">
      <div className="group card card-compact">
        <figure className="aspect-square relative h-[15rem] rounded-t-xl">
          <Image src={
            productImage
          } alt={product.name}
            className="w-full h-full group-hover:opacity-75 transition-opacity duration-200 ease-in-out"
            fill
          />
        </figure>
        <div className="absolute top-0 right-0 m-0 mt-2 mr-2 p-0">
          <label className="swap swap-flip p-0 m-0">
            <input type="checkbox" />
            <HeartIcon size={24}
              fillOpacity={0.5}
              className="swap-on fill-error stroke-error" />
            <HeartIcon size={24}
              className="swap-off stroke-primary/50"
            />
          </label>
        </div>
        <div className="badge badge-primary ml-2 mb-2 absolute top-0 left-0 mt-2 ml-2">NEW</div>
        <div className="flex p-1 px-2 m-0">
          <div className="w-2/3">
            <h2 className="group card-title text-base group-hover:opacity-75 transition-opacity duration-200 ease-in-out h-[3rem] line-clamp-2">
              {product.name}
            </h2>
          </div>
          <div className="grow" />
          <div className="card-action flex-1">
            <Button className="btn btn-sm"
              onClick={handleAddToCart}
            >
              <ShoppingCartIcon color="#fff" size={24} />
            </Button>
          </div>
        </div>

        <section id="price_card-footer"
          className="group flex justify-between p-2 m-0 mt-sm group-hover:opacity-75"
        >
          <PriceCard
            price={
              prices.length > 0 ?
                prices[0].unit_amount :
                "N/A"
            }
            currency={
              prices.length > 0 ?
                prices[0].currency :
                "N/A"
            }
          />
          <div className="grow" />

        </section>
      </div>
    </div>


  )
}

export default ProductCard;