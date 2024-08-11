"use client";
import ProductCard from '@/components/product';
import { generateProductLayoutObject } from '@/lib/actions';
import { LayoutClasses } from '@/types/layout';
import { useChat } from 'ai/react';
import { useState } from 'react';


const PlaygroundPage = () => {
  const [input, setInput] = useState('');
  const [layout, setLayout] = useState<LayoutClasses | null>(null);

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    // get the form data
    const formData = new FormData(event.currentTarget);
    const input = formData.get('input') as string;

    // generate the layout object
    const layoutPromptString = `Generate a layout object for a product card using Tailwind CSS classes based on the following input: "${input}"`;
    const layoutObject = await generateProductLayoutObject(layoutPromptString);
    setLayout(layoutObject);

  }

  return (
    <div className="flex flex-col w-full max-w-7xl h-screen py-24 mx-auto stretch border relative">
      <h1>Playground</h1>

      {
        (layout === null) ? (<div>Layout not generated yet</div>) : (
          <div>
            <h2>Layout</h2>
            <pre>{JSON.stringify(layout, null, 2)}</pre>
          </div>
        )
      }

      <ProductCard
        data={{
          id: '123',
          handle: 'product',
          name: 'Product Name',
          images: ['https://via.placeholder.com/400'],
          default_variant: {
            name: 'Default Variant',
            id: '123',
            prices: {
              data: [
                {
                  type: 'price',
                  id: '123',
                  currency: 'usd',
                  unit_amount: 1000,
                  unit_compare_amount: 1200,
                }
              ]
            }
          }
        }}
        layout={layout || {
          containerClass: 'bg-blue-100 transition-colors duration-300',
          imageClass: 'bg-blue-100',
          contentClass: 'bg-blue-100',
          titleClass: 'bg-blue-100',
          variantClass: 'bg-blue-100',
          priceClass: 'bg-blue-100',
          compareAtPriceClass: 'bg-blue-100',
          badgeClass: 'bg-blue-100',
        }}
      />
      <form onSubmit={handleSubmit}>
        <input
          className="absolute bottom-0 w-full max-w-4xl p-2 mb-8 border border-gray-300 rounded shadow-xl"
          name='input'
          placeholder="Say something..."
        />
        <button
          type="submit"
          className="absolute bottom-0 right-0 p-2 mb-8 mr-8 border border-gray-300 rounded shadow-xl"
        >
          Submit
        </button>
      </form>
    </div>
  );
}

export default PlaygroundPage;