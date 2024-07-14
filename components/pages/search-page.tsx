"use client";
import { useSearchParams } from 'next/navigation'
import { Suspense, useCallback, useEffect, useState } from 'react';

import algoliasearch, { SearchClient } from 'algoliasearch/lite';
import { TProduct } from '@/types/product';
import ProductDisplayList from '../product-display-list';

const algoliaAppId = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!;
const algoliaSearchApiKey = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY!;

let algoliaSearchClient = algoliasearch(algoliaAppId, algoliaSearchApiKey);

const SearchHeaderComponent = ({
  setSearchQuery
}
  : {
    setSearchQuery: (query: string) => void
  }
) => {
  const query = useSearchParams().get('q')
  if (query) {
    setSearchQuery(query)
  }
  return null
}

const SearchPageComponent = ({
  indexName
}: {
  indexName: string
}) => {
  const [searchQuery, setSearchQuery] = useState<string | null>(null)
  const [searchResults, setSearchResults] = useState<any[]>([])
  let searchClient: SearchClient = algoliaSearchClient

  const handleSearch = useCallback(async () => {
    if (!searchQuery) {
      return
    }
    const index = searchClient.initIndex(indexName)
    const { hits } = await index.search(searchQuery)
    setSearchResults(hits)
  }, [searchQuery, indexName, searchClient]);

  useEffect(() => {
    // TODO: Add debounce to handleSearch

    const fetchData = async () => {
      if (searchQuery) {
        await handleSearch()
      }
    }
    fetchData()
  }, [searchQuery, handleSearch])

  return (
    <div className='flex flex-1 flex-col w-full'>
      <Suspense fallback={<div>Loading...</div>}>
        <SearchHeaderComponent {...{ setSearchQuery }} />
      </Suspense>

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