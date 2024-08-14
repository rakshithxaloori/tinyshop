"use client";

import { Product } from "@tinyshop/tinyshop-node/interfaces/product";
import ProductCardStructure, { ProductLayout } from "./structure/product";
import { useState } from "react";


const AIProduct = ({ product, layout }:
  { product: Product; layout: ProductLayout }
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
    <ProductCardStructure
      data={data}
      actions={actions}
      layout={layout}
    />
  )
}

export default AIProduct;