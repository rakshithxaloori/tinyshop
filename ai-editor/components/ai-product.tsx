"use client";

import { Product } from "@tinyshop/tinyshop-node/interfaces/product";
import ProductCardStructure, { ProductLayout } from "./structure/product";
import { useState } from "react";
import WishlistStructure from "./structure/wishlist";
import AddToCartButtonStructure from "./structure/add-to-cart-btn";
import IconButtonStructure from "./structure/icon-btn";
import PriceStructure from "./structure/price";
import dynamic from "next/dynamic";

const NoSSRQuantityStructure = dynamic(() => import("@/components/structure/quantity"), {
  ssr: false,
  loading: () => <div className="h-6 w-6 animate-spin border-2 rounded-full border-base-300 border-t-primary" />
});


const AIProduct = ({ product, layout, theme }:
  { product: Product; layout: ProductLayout; theme: string }
) => {
  const productImage = product?.images && product.images[0] ? product.images[0] : "/api/placeholder/400/400"
  const [cartProductQuantity, setCartProductQuantity] = useState<number>(0)

  // @ts-ignore
  const itemPrice = product?.default_variant?.prices?.data[0].unit_amount
  // @ts-ignore
  const itemCurrency = product?.default_variant?.prices?.data[0].currency

  const data = {
    id: product.id,
    productImage,
    name: product.name,
    badgeTitle: "NEW",
    quantity: cartProductQuantity,
    price: itemPrice,
    currency: itemCurrency
  }

  const actions = {
    handleCardClick: () => { },
    handleAddToCart: () => { setCartProductQuantity(cartProductQuantity + 1) }
  }

  return (
    <div data-theme={theme}>
      <ProductCardStructure
        data={data}
        actions={actions}
        layout={layout}
        wishlist={WishlistStructure}
        addToCartButton={AddToCartButtonStructure}
        iconButton={IconButtonStructure}
        priceCard={PriceStructure}
        quantityDisplay={NoSSRQuantityStructure}
      />
    </div>
  )
}

export default AIProduct;