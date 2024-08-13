"use client";
import ProductCard from '@/components/product';
import { generateProductLayoutObject } from '@/lib/actions';
import { LayoutClasses } from '@/types/layout';
import { css } from '@emotion/css';
import { useChat } from 'ai/react';
import { SendHorizontalIcon } from 'lucide-react';
import Image from 'next/image';
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
    <div className="flex flex-col w-full max-w-7xl h-screen py-4 mx-auto stretch relative">
      <div className='flex flex-col h-full'>
        <div className='h-fit text-2xl text-center'>
          {
            isQuerying ? 'Querying...' : query
          }
        </div>
        <div className='flex flex-1 items-center'>
          {/* {
            JSON.stringify(layout, null, 2)
          } */}

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
              containerClass: '',
              imageClass: 'bg-blue-100 w-full aspect-square',
              contentClass: 'bg-blue-100',
              titleClass: 'bg-blue-100',
              variantClass: 'bg-blue-100',
              priceClass: 'bg-blue-100',
              compareAtPriceClass: 'bg-blue-100',
              badgeClass: 'bg-blue-100',
            }}
          />


        </div>
      </div>

      <div className='z-40 flex w-full origin-bottom justify-center sm:-translate-y-1'>

        <div className="relative z-10 flex min-h-fit w-full items-center justify-center gap-2 rounded-3xl bg-gray-800 px-2 shadow-lg transition-all duration-300 sm:shadow-black/40 max-w-lg sm:max-w-xl xl:max-w-2xl">
          <div className="hidden items-center justify-center rounded-l-full sm:flex">
            <Image alt="Avatar"
              src="https://vercel.com/api/www/avatar/6Ysz26mlstSJz7qUXt2n8opm?s=64"
              height="32" width="32" className="relative flex shrink-0 rounded-full"

            />
          </div>
          <div className="relative flex w-full min-w-0 flex-1 items-center self-end border-gray-700 pl-2 sm:border-l">
            <form className="h-full w-full" onSubmit={handleSubmit} ref={formRef}>
              <div className="relative flex w-full flex-1 items-center justify-center gap-2 transition-all duration-300">
                <label className="sr-only">Prompt</label>
                <div className="relative flex w-full min-w-0 flex-1 justify-between self-start min-h-[3rem] items-center">
                  <textarea
                    className="min-h-[1.5rem] h-[1rem] flex-[1_0_50%] resize-none border-0 bg-transparent text-sm leading-relaxed shadow-none outline-none ring-0 [scroll-padding-block:0.75rem] selection:bg-teal-300 selection:text-black disabled:bg-transparent disabled:opacity-80 text-white placeholder:text-zinc-400 w-full"
                    name='input'
                    placeholder={query || "Make the heading larger and darker"}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        formRef.current?.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
                      }
                    }}
                  />
                </div>
                <div className="flex">
                  {
                    isQuerying ? <div className="h-6 w-6 animate-spin rounded-full border-4 border-gray-800 border-t-white" /> :
                      <button className="shrink-0 whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 flex items-center justify-center bg-transparent text-white hover:bg-gray-800 focus-visible:bg-gray-800 focus-visible:ring-0 h-8 w-8 rounded-full" id="send-button" type="submit">
                        <span className="sr-only">Send</span>
                        <SendHorizontalIcon className="h-6 w-6" />
                      </button>

                  }
                </div>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div >
  );
}

export default PlaygroundPage;