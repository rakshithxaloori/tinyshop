
// The product card component consists of
// 1. product image
// 2. product name
// 3. product price
// 4. product discount
// 5. product rating
// 6. Cart actions
// 7. Wishlist actions
"use client";
import { Button } from "../ui/button";
import PriceCard from "@/components/price/price-card-v1";
import { useRouter } from "next/navigation";
import { TPriceUI, TProductUICard } from "@/types/product";
import WishlistItem from "./wishlist";
import useCartStore from "@/store/cart";
import dynamic from "next/dynamic";
import { ShoppingCartIcon } from "lucide-react";
import { useSearchQuery } from "../hooks/search";
import ProductCardStructure, { nullProductLayout, ProductLayout } from "./card-structure";
import { cn } from "@/lib/utils";
import { PriceTypeEnum } from "@tinyshop/tinyshop-node/interfaces/price";

const disableOneTime = process.env.NEXT_PUBLIC_DISABLE_ONE_TIME! === "true";

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

const IconButton = ({ className, onClick }: { className?: string, onClick: React.MouseEventHandler<HTMLButtonElement> }) => {
  return (
    <Button className={cn("btn btn-sm", className)}
      onClick={onClick}
    >
      <ShoppingCartIcon color="#fff" size={24} />
    </Button>

  )
}

const AddToCartButton = ({ className, onClick }: { className?: string, onClick: React.MouseEventHandler<HTMLButtonElement> }) => {
  return (
    <Button variant="outline"
      className={cn("w-full rounded-full border-primary text-primary hover:bg-primary hover:text-primary-content", className)}
      onClick={onClick}
    >
      Add
    </Button>
  )
}

const ProductCard = ({ product,
  fallbackOptions,
  layout
}: {
  product: TProductUICard;
  fallbackOptions: any;
  layout: ProductLayout;
}) => {
  const { image } = fallbackOptions;
  const productImage = product?.images && product.images[0] ? product.images[0] : image;
  const prices: TPriceUI[] = product?.default_variant?.prices ? processPricesResponse(product?.default_variant?.prices?.data) : [] as any;
  const oneTimePrice = prices.find(price => price.type === PriceTypeEnum.ONE_TIME) ?? prices[0];
  const subscriptionPrice = prices.find(price => price.type === PriceTypeEnum.RECURRING) ?? prices[0];

  const router = useRouter();
  const cartStore = useCartStore();
  const { addItem, getProduct } = cartStore;
  const cartProductQuantity = getProduct(product.id).quantity ?? 0;
  const { clearQuery } = useSearchQuery();

  const cartItemChain = {
    priceId: prices.length > 0 ? (
      disableOneTime ? subscriptionPrice.id :
        oneTimePrice.id) : "N/A",
    productId: product.id,
    variantId: product?.default_variant?.id ?? "N/A"
  }

  const itemPrice = prices.length > 0 ?
    (disableOneTime ?
      subscriptionPrice.unit_amount ?? "N/A" :
      oneTimePrice.unit_amount ?? "N/A") :
    "N/A"
  const itemCurrency = prices.length > 0 ?
    oneTimePrice.currency :
    "N/A"

  const cartItemDisplay = {
    image: productImage,
    name: product.name,
    variantName: product?.default_variant?.name ?? null,
    isSubscription: disableOneTime,
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

  const actions = {
    handleCardClick: handleLinkClick,
    handleAddToCart
  }

  const data = {
    id: product.id,
    productImage,
    name: product.name,
    badgeTitle: "NEW",
    quantity: cartProductQuantity,
    price: itemPrice,
    currency: itemCurrency
  }

  if (!layout) {
    layout = nullProductLayout
  }

  return (
    <ProductCardStructure
      data={data}
      layout={layout}
      actions={actions}
      quantityDisplay={NoSSRCartBagDisplay}
      priceCard={PriceCard}
      wishlist={WishlistItem}
      iconButton={IconButton}
      addToCartButton={AddToCartButton}
    />
  )
}

export default ProductCard;