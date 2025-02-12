"use client";

import { CurrencyString } from '@/components/price/currency-icon'
import { deleteCartId } from '@/lib/cookie/cart';
import { getSubscriptionItems } from '@/lib/server-actions'
import useCartStore from '@/store/cart';
import { TCheckoutItem } from '@/types/product'
import Image from 'next/image'
import { useSearchParams } from 'next/navigation'
import React, { use, useEffect, useState } from 'react'

const ThanksPage = () => {
  const subscriptionId = useSearchParams().get('subId')
  const [subscriptionItems, setSubscriptionItems] = useState<TCheckoutItem[]>([])
  const clearCart = useCartStore(state => state.clearCart)

  useEffect(() => {
    async function fetchData() {
      if (subscriptionId) {
        const items = await getSubscriptionItems(subscriptionId)
        setSubscriptionItems(items as any)
        deleteCartId();
        clearCart();
      }
    }
    fetchData()
  }, [subscriptionId, clearCart])

  const total = subscriptionItems.reduce((acc, item) => acc + (Number(item.unitAmount) / 100 * item.quantity), 0).toFixed(2)

  return (
    <div>
      <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 lg:grid lg:max-w-7xl lg:gap-x-8 lg:px-8 lg:py-32 xl:gap-x-24">
        <div className="lg:col-start-1">
          <h1 className="text-sm font-medium text-success">Payment successful</h1>
          <p className="mt-2 text-4xl font-bold tracking-tight text-primary-content sm:text-5xl">Thanks for ordering</p>
          <p className="mt-2 text-base text-gray-500">We appreciate your order, we’re currently processing it. So hang tight and we’ll send you confirmation very soon!</p>

          <ul role="list" className="mt-6 divide-y divide-primary border-t border-gray-200 text-sm font-medium text-primary-content/70">
            {
              subscriptionItems.map((item: TCheckoutItem, index) => (
                <li key={index} className="flex space-x-6 py-6">
                  <div className="relative h-24 w-24">
                    <Image src={item.image} alt={item.productName}
                      width={96}
                      height={96}
                      className="aspect-square rounded-lg"
                    />
                  </div>
                  <div className="flex-auto space-y-1">
                    <h3 className="text-primary-content">
                      {item.productName}
                    </h3>
                    <p>{item.variantName}</p>
                    <p>Price: <CurrencyString currency="inr" />{" "}{(Number(item.unitAmount) / 100).toFixed(2)}</p>
                    <p>Qty: {item.quantity}</p>
                  </div>
                  <p className="flex-none font-medium text-gray-900">
                    <CurrencyString currency="inr" />{" "}
                    {(Number(item.unitAmount) / 100 * item.quantity).toFixed(2)}
                  </p>
                </li>
              ))
            }
          </ul>

          <dl className="space-y-6 border-t border-primary pt-sm text-sm font-medium text-gray-500">
            <div className="flex justify-between">
              <dt>Subtotal</dt>
              <dd className="text-primary-content">
                <CurrencyString currency="inr" />{" "}
                {total}
              </dd>
            </div>

            <div className="flex justify-between">
              <dt>Shipping</dt>
              <dd className="text-primary-content">
                <CurrencyString currency="inr" />{" "}
                {0}
              </dd>
            </div>

            <div className="flex justify-between">
              <dt>Taxes</dt>
              <dd className="text-primary-content">
                <CurrencyString currency="inr" />{" "}
                {0}
              </dd>
            </div>

            <div className="flex items-center justify-between border-t border-primary pt-sm text-primary-content">
              <dt className="text-base-content">Total</dt>
              <dd className="text-base-content">
                <CurrencyString currency="inr" />{" "}
                {total}
              </dd>
            </div>
          </dl>

        </div>
      </div>
    </div>
  )
}

export default ThanksPage