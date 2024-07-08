"use client";
import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react';

const SearchImpl = () => {
  const query = useSearchParams().get('q')
  return (
    <div className="min-h-full">
      <h1 className="text-2xl text-center">Searching for &quot;{query}&quot;</h1>
    </div>
  )
}

const SearchPageComponent = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchImpl />
    </Suspense>
  )
}

export default SearchPageComponent