"use client";
import { useEffect, useState } from 'react';

import algoliasearch, { SearchClient } from 'algoliasearch/lite';
import { TProduct } from '@/types/product';
import { useSearchQuery } from '../hooks/search';
import ProductDisplayList from '../product-display-list';

const algoliaAppId = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!;
const algoliaSearchApiKey = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY!;
const shopName = process.env.NEXT_PUBLIC_SHOP_NAME!;

let algoliaSearchClient: SearchClient = algoliasearch(algoliaAppId, algoliaSearchApiKey);

const SearchPageComponent = ({
  indexName
}: {
  indexName: string
}) => {
  const { query: searchQuery } = useSearchQuery()
  const [searchResults, setSearchResults] = useState<any[]>([])
  const filter = `shopId:${shopName}`

  useEffect(() => {
    // TODO: Add debounce to handleSearch
    const handleSearch = async () => {
      if (!searchQuery) {
        return
      }
      const index = algoliaSearchClient.initIndex(indexName)
      const { hits } = await index.search(searchQuery, {
        filters: filter
      })
      return hits
    }

    const fetchData = async () => {
      if (searchQuery) {
        const results = await handleSearch()
        setSearchResults(results as any[])
      }
    }
    fetchData()
  }, [searchQuery, indexName, filter])

  return (
    <div className='flex flex-1 flex-col w-full'>
      <h1 className="mt-lg mb-sm text-3xl font-bold leading-none tracking-tight text-base-content">
        Search results for &quot;{searchQuery}&quot;
      </h1>

      <ProductDisplayList
        name="All Products"
        products={searchResults as TProduct[]}
      />
    </div>
  )
}

export default SearchPageComponent