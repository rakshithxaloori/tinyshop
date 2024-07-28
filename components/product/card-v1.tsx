
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
import { Button } from "../ui/button";
import PriceCard from "@/components/price/price-card-v1";
import { useRouter } from "next/navigation";
import { TPriceUI, TProductUICard } from "@/types/product";
import WishlistItem from "./wishlist";
import useCartStore from "@/store/cart";
import dynamic from "next/dynamic";
import { ShoppingBagIcon, ShoppingCartIcon } from "lucide-react";
import { useSearchQuery } from "../hooks/search";

const NoSSRCartBagDisplay = dynamic(() => import("../cart-bag-display"), {
  ssr: false,
  loading: () => <div className="h-6 w-6 animate-spin border-2 rounded-full border-base-300 border-t-primary" />
});

const processPricesResponse = (prices: any): TPriceUI => {
  // Prices are returned as an array of objects
  // return the currency, the unit_amount and the unit_compare_amount
  // if available
  return prices.map((price: any) => {
    const { currency, unit_amount, unit_compare_amount, id, type } = price;
    return {
      type,
      id,
      currency,
      unit_amount,
      unit_compare_amount
    }
  });
}

const ProductCard = ({ product,
  fallbackOptions
}: {
  product: TProductUICard;
  fallbackOptions: any;
}) => {
  const { image } = fallbackOptions;
  const productImage = product?.images && product.images[0] ? product.images[0] : image;
  const prices: TPriceUI[] = product?.default_variant?.prices ? processPricesResponse(product?.default_variant?.prices?.data) : [] as any;
  const oneTimePrice = prices.find(price => price.type === "one_time") ?? prices[0];

  const router = useRouter();
  const cartStore = useCartStore();
  const { addItem, getProduct } = cartStore;
  const cartProductQuantity = getProduct(product.id).quantity ?? 0;
  const { clearQuery } = useSearchQuery();

  const cartItemChain = {
    priceId: prices.length > 0 ? oneTimePrice.id : "N/A",
    productId: product.id,
    variantId: product?.default_variant?.id ?? "N/A"
  }

  const itemPrice = prices.length > 0 ?
    oneTimePrice.unit_amount ?? "N/A" :
    "N/A"
  const itemCurrency = prices.length > 0 ?
    oneTimePrice.currency :
    "N/A"

  const cartItemDisplay = {
    image: productImage,
    name: product.name,
    variantName: product?.default_variant?.name ?? null,
    isSubscription: false,
    price: itemPrice,
    currency: itemCurrency
  }

  const handleAddToCart: React.MouseEventHandler<HTMLButtonElement> = (event) => {
    event.preventDefault();
    event.stopPropagation();
    addItem(cartItemChain, cartItemDisplay, 1);
  };

  const handleLinkClick = () => {
    router.push(`/products/${product.handle}`);
    clearQuery();
  };

  return (
    <div onClick={handleLinkClick}
      className="card-wrapper cursor-pointer border-primary/60 hover:border-primary hover:m-1 transition-all duration-100 ease-linear bg-base-100 border-2 rounded-xl">
      <div className="group card card-compact">
        <figure className="relative aspect-square rounded-t-xl">
          <Image src={
            productImage
          } alt={product.name}
            className="w-full h-full group-hover:opacity-75 group-focus:opacity-100 transition-opacity duration-200 ease-in-out"
            fill
          />
        </figure>
        <WishlistItem product={product} />
        <div className="badge badge-primary ml-2 mb-2 absolute top-0 left-0 mt-2 ml-2">NEW</div>
        <div className="flex m-0 mt-md mx-md">
          <div className="w-full">
            <h2 className="group card-title text-base group-hover:opacity-75 transition-opacity duration-200 ease-in-out h-[3rem] line-clamp-2">
              {product.name}
            </h2>
          </div>
          <div className="grow" />
          <div className="card-action flex-1 hidden md:block">
            <Button className="btn btn-sm"
              onClick={handleAddToCart}
            >
              <ShoppingCartIcon color="#fff" size={24} />
            </Button>
          </div>
        </div>

        <section id="price_card-footer"
          className="group flex justify-between p-2 m-0 mt-xs md:mt-sm  group-hover:opacity-75"
          suppressHydrationWarning={true}
        >
          <PriceCard
            price={itemPrice}
            currency={itemCurrency}
          />

          <div className="grow" />

          <NoSSRCartBagDisplay quantity={cartProductQuantity}
            cx={cartProductQuantity > 0 ? "block" : "hidden"}
          />
        </section>

        <section id="mobile_card-footer"
          className="visible md:hidden my-sm"
        >
          <div className="card-action w-full px-2">
            <Button variant="outline"
              className="w-full rounded-full border-primary text-primary"
              onClick={handleAddToCart}
            >
              Add
            </Button>
          </div>
        </section>
      </div>
    </div>
  )
}

export default ProductCard;

export type { TProductUICard };