"use client";
import ProductCard from '@/components/product';
import { generateProductLayoutObject } from '@/lib/actions';
import { LayoutClasses } from '@/types/layout';
import { css } from '@emotion/css';
import { useChat } from 'ai/react';
import { GitCommitHorizontalIcon, PaletteIcon, RefreshCwIcon, SaveAllIcon, SaveIcon, SendHorizontalIcon, ThumbsDownIcon } from 'lucide-react';
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
    <div className="flex flex-col h-[calc(100vh-100px)] h-[calc(100svh-60px)] md:h-[calc(100vh-64px)] md:h-[calc(100svh-64px)]">
      <div className="flex flex-1 flex-col gap-3 bg-white border-t lg:border-t-0 p-4 pb-2 pt-3 lg:border-t-0 lg:pt-0">

        <div className="flex flex-1 flex-col items-start gap-4 md:flex-row">


          <div className='relative flex size-full flex-1 flex-col gap-3 sm:order-2 lg:overflow-hidden lg:rounded-xl lg:p-3 lg:bg-gray-50'>
            <div>
              <div className="flex w-full items-center gap-8" data-id="toolbar-top">
                <div className="hidden flex-1 overflow-hidden lg:flex">
                  <div className="flex items-center justify-start gap-3 overflow-hidden" data-id="commit-prompt">
                    <div className="flex flex-1 items-center gap-2 overflow-hidden">
                      <a className="flex-none" href="/">
                        <span className="sr-only">Link to eulerkochy&apos;s v0.dev Profile</span>
                        <Image alt="Avatar"
                          src="https://vercel.com/api/www/avatar/6Ysz26mlstSJz7qUXt2n8opm?s=64"
                          height="32" width="32" className="relative flex shrink-0 rounded-full"
                        />
                      </a>
                      <button className="relative max-w-full overflow-hidden" title="make the heading larger">
                        <div className="relative flex-1 overflow-hidden text-ellipsis rounded-2xl bg-[#ebebeb] px-3 py-1">
                          <span className="text-left text-sm line-clamp-1 break-all">
                            {
                              isQuerying ? 'Querying...' : query
                            }
                          </span>
                        </div>
                      </button>
                      <div className="flex items-center gap-2">
                        <span className="flex items-center justify-center" data-state="closed">
                          <button className="inline-flex shrink-0 items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 text-gray-500 hover:text-gray-900 h-[28px] w-[28px] rounded-full p-0 hover:bg-[#f2f2f2]" data-id="toolbar-downvote-button">
                            <span className="sr-only">Downvote Result</span>
                            <ThumbsDownIcon className="h-4 w-4" />
                          </button>
                        </span>
                      </div>
                    </div>
                    <div className="ml-auto flex items-center gap-2 lg:ml-0">
                      <button className="shrink-0 items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 text-gray-500 hover:text-gray-900 flex h-[28px] w-[28px] rounded-full p-0 hover:bg-[#f2f2f2]" data-state="closed">
                        <RefreshCwIcon className="h-4 w-4" />
                        <span className="sr-only">Regenerate
                        </span>
                      </button>
                    </div>
                  </div>
                </div>
                <div className="flex w-full items-center gap-2 lg:ml-auto lg:w-auto">
                  <div className="box-content flex h-6 items-center gap-2 rounded-md border border-gs-gray-alpha-400 bg-white p-1">
                    {/* <!-- Desktop Button --> */}
                    <button className="shrink-0 items-center justify-center ... hidden lg:flex bg-gray-100 text-gray-900">
                      <span className="sr-only">Desktop</span>
                      <svg className="lucide lucide-monitor h-4 w-4">...</svg>
                    </button>
                    {/* <!-- Tablet Button --> */}
                    <button className="shrink-0 items-center justify-center ... hidden lg:flex">
                      <span className="sr-only">Tablet</span>
                      <svg className="lucide lucide-tablet h-4 w-4">...</svg>
                    </button>
                    {/* <!-- Mobile Button --> */}
                    <button className="shrink-0 items-center justify-center ... hidden lg:flex">
                      <span className="sr-only">Mobile</span>
                      <svg className="lucide lucide-smartphone h-4 w-4">...</svg>
                    </button>
                    {/* <!-- Divider --> */}
                    <div className="shrink-0 bg-gray-200 w-[1px] hidden h-5 lg:block"></div>
                    {/* <!-- Full Screen Button --> */}
                    <button className="inline-flex shrink-0 items-center justify-center ...">
                      <span className="sr-only">Full Screen</span>
                      <svg className="lucide lucide-maximize h-4 w-4">...</svg>
                    </button>
                    {/* <!-- Divider --> */}
                    <div className="shrink-0 bg-gray-200 w-[1px] hidden h-5 lg:block"></div>
                    {/* <!-- History Button --> */}
                    <button className="inline-flex shrink-0 items-center justify-center ... lg:hidden">
                      <span className="sr-only">History</span>
                      <svg className="lucide lucide-history h-4 w-4">...</svg>
                    </button>
                    {/* <!-- More Button --> */}
                    <button className="inline-flex shrink-0 items-center justify-center ...">
                      <span className="sr-only">More</span>
                      <svg className="lucide lucide-ellipsis h-4 w-4">...</svg>
                    </button>
                  </div>
                  <div className="flex flex-1 gap-2 @container sm:@container-normal">
                    {/* <!-- Theme Button --> */}
                    <button className="inline-flex shrink-0 items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:bg-gray-100 gap-1 py-1 text-[#666666] hover:text-[#171717] px-2 h-8 w-auto rounded-md border bg-white ml-auto">
                      <span className="sr-only sm:not-sr-only">Theme</span>
                      <PaletteIcon className="h-4 w-4" />
                    </button>
                    {/* <!-- Code Button --> */}
                    <button className="inline-flex shrink-0 items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground shadow hover:bg-primary/90 h-8 px-3 py-2 gap-1.5 @[95px]:w-[95px] sm:w-[95px] ml-0">
                      <span className="hidden @[95px]:inline-block sm:inline-block">Publish</span>
                      <SaveIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div className='flex-1'>

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
            <div className="w-full lg:hidden" data-id="toolbar-bottom">
              <div className="flex items-center justify-start gap-3 overflow-hidden" data-id="commit-prompt">
                <div className="flex flex-1 items-center gap-2 overflow-hidden">
                  <a className="flex-none" href="/">
                    <span className="sr-only">Link to eulerkochy&apos;s v0.dev Profile</span>
                    <Image alt="Avatar"
                      src="https://vercel.com/api/www/avatar/6Ysz26mlstSJz7qUXt2n8opm?s=64"
                      height="32" width="32" className="relative flex shrink-0 rounded-full"
                    />
                  </a>
                  <button className="relative max-w-full overflow-hidden" title={query}>
                    <div className="relative flex-1 overflow-hidden text-ellipsis rounded-2xl bg-[#ebebeb] px-3 py-1">
                      <span className="text-left text-sm line-clamp-1 break-all">{query}</span>
                    </div></button><div className="flex items-center gap-2">
                    <span className="flex items-center justify-center" data-state="closed">
                      <button className="inline-flex shrink-0 items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 text-gray-500 hover:text-gray-900 h-[28px] w-[28px] rounded-full p-0 hover:bg-[#f2f2f2]" data-id="toolbar-downvote-button">
                        <span className="sr-only">Downvote Result</span>
                        <ThumbsDownIcon className="h-4 w-4" />
                      </button>
                    </span>
                  </div>
                </div>
                <div className="ml-auto flex items-center gap-2 lg:ml-0">
                  <button className="shrink-0 items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 text-gray-500 hover:text-gray-900 flex h-[28px] w-[28px] rounded-full p-0 hover:bg-[#f2f2f2]" data-state="closed">
                    <RefreshCwIcon className="h-4 w-4" />
                    <span className="sr-only">Regenerate
                    </span>
                  </button>
                </div>
              </div>
            </div>
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
      </div>
    </div >
  );
}

export default PlaygroundPage;