"use client";
import ProductCard from '@/components/product';
import { generateProductLayoutObject } from '@/lib/actions';
import { LayoutClasses } from '@/types/layout';
import { useChat } from 'ai/react';
import { useRef, useState } from 'react';


const PlaygroundPage = () => {
  const [query, setQuery] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);

  const [layout, setLayout] = useState<LayoutClasses | null>(null);

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setIsQuerying(true);
    // disable the form


    // get the form data
    const formData = new FormData(event.currentTarget);
    const input = formData.get('input') as string;

    // generate the layout object
    const layoutPromptString = `Generate a layout object for a product card using Tailwind CSS classes based on the following input: "${input}"`;
    const layoutObject = await generateProductLayoutObject(layoutPromptString);
    setIsQuerying(false);
    setLayout(layoutObject);

    setQuery(input)

    formRef.current?.reset();
  }

  return (
    <div className="flex flex-col w-full max-w-7xl h-screen py-24 mx-auto stretch relative">
      <div className='flex flex-col h-full'>
        <div className='h-fit text-2xl text-center'>
          {
            isQuerying ? 'Querying...' : query
          }
        </div>
        <div className='flex flex-1 items-center'>
          {(
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
          )
          }

        </div>
      </div>

      <form onSubmit={handleSubmit} className='w-full mx-auto'
        ref={formRef}
      >
        <input
          className="w-full p-2 border border-gray-300 rounded shadow-xl"
          name='input'
          placeholder="Say something..."
        />
      </form>
    </div>
  );
}

export default PlaygroundPage;