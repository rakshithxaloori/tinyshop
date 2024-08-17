"use client";
import { generateProductLayoutObject, LayoutHistory, uploadLayoutInformationToMongo } from '@/lib/actions';
import { Product } from '@tinyshop/tinyshop-node/interfaces/product';
import { RefreshCwIcon, SaveIcon, SendHorizontalIcon, ThumbsDownIcon } from 'lucide-react';
import Image from 'next/image';
import { useRef, useState } from 'react';
import { nullProductLayout, ProductLayout } from '../structure/product';
import AIProduct from '@/components/ai-product';
import { Themes } from '@/components/themes';
import { Button } from '@/components/ui/button';

type UIMessage = {
  input: string;
  layout: ProductLayout;
}

type UIHistory = {
  index: number;
  message: UIMessage | null;
}

const AiEditorPage = ({
  data
}: {
  data: Product[]
}) => {
  const [isQuerying, setIsQuerying] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  const [theme, setTheme] = useState<string>('light');
  const [messages, setMessages] = useState<UIMessage[]>([]);
  const [selectedHistory, setSelectedHistory] = useState<UIHistory>({ index: -1, message: null });

  const onHistorySelect = (index: number) => {
    setSelectedHistory({
      index,
      message: messages[index]
    });
  }

  const handlePublish = async (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.preventDefault();
    const mongoLayoutInformation = {
      layout: selectedHistory.message?.layout || nullProductLayout,
      theme
    }
    console.log('Publishing to mongo:', mongoLayoutInformation);
    setIsPublishing(true);
    await uploadLayoutInformationToMongo(mongoLayoutInformation);
    setIsPublishing(false);
  }

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
    const layoutPromptString = `${input}`;
    let generatedLayoutObject;
    if (messages.length === 0) {
      generatedLayoutObject = await generateProductLayoutObject(layoutPromptString, {} as LayoutHistory, theme);
    } else {
      generatedLayoutObject = await generateProductLayoutObject(layoutPromptString, {
        messages: messages.map((msg) => msg.input),
        lastGeneratedObject: messages[messages.length - 1]?.layout || null
      },
        theme
      );
    }
    setIsQuerying(false);
    console.log('Generated layout object:', generatedLayoutObject);
    const message = {
      input,
      layout: generatedLayoutObject
    }
    setMessages((msgArr) => [...msgArr, message]);
    setSelectedHistory((prev) => ({ index: prev.index + 1, message }));


    formRef.current?.reset();
  }

  return (
    <div className="flex flex-col mt-2 h-[calc(100vh-108px)] h-[calc(100svh-68px)] md:h-[calc(100vh-72px)] md:h-[calc(100svh-72px)]">
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
                              isQuerying ? 'Querying...' : selectedHistory.message?.input
                            }
                          </span>
                        </div>
                      </button>
                      <div className="flex items-center gap-2 hidden">
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
                  <div className="box-content flex h-6 items-center gap-2 rounded-md border border-gs-gray-alpha-400 bg-white p-1 hidden">
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
                    <Themes selectedTheme={theme} setSelectedTheme={setTheme} />
                    {/* <!-- Code Button --> */}
                    <button className="inline-flex shrink-0 items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-sh-primary text-sh-primary-foreground shadow hover:bg-sh-primary/90 h-8 px-3 py-2 gap-1.5 @[95px]:w-[95px] sm:w-[95px] ml-0"
                      onClick={handlePublish}
                    >
                      <span className="hidden @[95px]:inline-block sm:inline-block">Publish</span>
                      {isPublishing ? <div className="h-4 w-4 animate-spin rounded-full border-4 border-gray-800 border-t-white" /> :
                        <SaveIcon className="h-4 w-4" />}
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div className='flex-1'>
              <div className="my-lg grid grid-cols-2 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {
                  data.map((product) => (
                    <AIProduct
                      key={product.id}
                      product={product}
                      layout={selectedHistory.message?.layout || nullProductLayout}
                      theme={theme}
                    />
                  ))
                }
              </div>

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
                  <button className="relative max-w-full overflow-hidden" title={selectedHistory.message?.input}>
                    <div className="relative flex-1 overflow-hidden text-ellipsis rounded-2xl bg-[#ebebeb] px-3 py-1">
                      <span className="text-left text-sm line-clamp-1 break-all">
                        {isQuerying ? 'Querying...' : selectedHistory.message?.input}
                      </span>
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
          <div className='hidden shrink-0 origin-left select-none flex-col overflow-hidden rounded-lg bg-gray-50 py-2 transition-all duration-300 ease-out @container lg:flex max-h-[calc(100vh-190px)] h-auto w-[44px]'>
            <div className="no-scrollbar flex flex-1 flex-col-reverse overflow-auto">
              <div className="flex flex-col gap-3 px-[6px] py-1">
                {
                  messages.map((msg, index) => (
                    <Button key={index} variant="outline" className={`${index === selectedHistory.index ? 'ring-2' : ''} text-sm font-semibold`}
                      onClick={() => onHistorySelect(index)}
                      size="sm"
                    >
                      v{index + 1}
                    </Button>
                  ))
                }
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
                      placeholder={selectedHistory.message?.input || "Make the heading larger and darker"}
                      disabled={isQuerying}
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
    </div>
  );
}

export default AiEditorPage;