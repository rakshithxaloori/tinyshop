"use server";

import { cn } from "@/lib/utils";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface TabsSectionProps {
  data: TProductTabs[] | null
}
import { ImageAndTextTabContent, TextOnlyTabContent } from "@/template/tab-content/basic";
import { TProductTabs } from "@/types/product";

type TabType = "text" | "text-image" | "image"
type TabContent = string | {
  image: {
    src: string
    alt: string
  }
  text: string
} | {
  src: string
  alt: string
}

type Tab = {
  name: string
  id: string
  type: TabType
  content: TabContent
}

const tabList = [
  {
    name: "How to use",
    id: "how-to-use",
    type: "text",
    content: "This is how you use this product. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eligendi non quis exercitationem culpa nesciunt nihil aut nostrum explicabo reprehenderit optio amet ab temporibus asperiores quasi cupiditate. Voluptatum ducimus voluptates voluptas?",
  },
  {
    name: "Ingredients",
    id: "ingredients",
    type: "text-image",
    content: {
      image: {
        src: "https://images.unsplash.com/photo-1720692739658-ee952b1aebb1?q=80&w=2787&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        alt: "Ingredients"
      },
      text: "This is the list of ingredients. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eligendi non quis exercitationem culpa nesciunt nihil aut nostrum explicabo reprehenderit optio amet ab temporibus asperiores quasi cupiditate. Voluptatum ducimus voluptates voluptas?"
    }
  }
]

const tabSpec = {
  defaultTab: "how-to-use",
  tabs: tabList
}

function cleanString(str: string): string {
  return str
    .replace(/\s+/g, ' ')  // Replace multiple whitespace characters with a single space
    .replace(/\n/g, '')    // Remove all newline characters
    .trim();               // Remove leading and trailing whitespace
}

function constructTabSpec(tabs: TProductTabs[]): any {
  const tabList = tabs.map((tab, index) => {
    const name: string = cleanString(tab.title)
    // replace all special characters with a hyphen
    const id: string = name.toLowerCase().replace(/\s+/g, "-").replace(/[^a-z0-9-]/g, "")
    // get tab content type by inspecting the content
    let type: TabType = "text"
    let content: TabContent = tab.content
    if (typeof tab.content === 'object') {
      if (tab.content.image && tab.content.text) {
        type = "text-image"
        content = {
          image: {
            src: tab.content.image.src,
            alt: tab.content.image.alt
          },
          text: tab.content.text
        }
      } else if (tab.content.image) {
        type = "image"
        content = {
          src: tab.content.image.src,
          alt: tab.content.image.alt
        }
      } else if (tab.content.text) {
        type = "text"
        content = tab.content.text
      }
    }

    return {
      name,
      id,
      type,
      content
    }
  })
  return {
    defaultTab: tabList[0].id,
    tabs: tabList
  }
}

const TabsBuilder = ({ data }: { data: TProductTabs[] }) => {
  const numtabs = data.length
  const tailwindClass =
    (numtabs === 1) ? "grid-cols-1" :
      (numtabs === 2) ? "grid-cols-2" :
        (numtabs === 3) ? "grid-cols-3" :
          (numtabs === 4) ? "grid-cols-4" :
            (numtabs === 5) ? "grid-cols-5" :
              (numtabs === 6) ? "grid-cols-6" :
                (numtabs === 7) ? "grid-cols-7" :
                  (numtabs === 8) ? "grid-cols-8" :
                    (numtabs === 9) ? "grid-cols-9" :
                      (numtabs === 10) ? "grid-cols-10" :
                        "grid-cols-11"

  const { defaultTab, tabs } = constructTabSpec(data)

  return (
    <Tabs defaultValue={defaultTab}
      className="w-full min-h-full flex flex-1 flex-col border-2 border-primary rounded-lg shadow-sm">
      <TabsList className={
        cn("grid w-full",
          tailwindClass,
        )
      }>
        {tabs.map((tab: any) => (
          <TabsTrigger key={tab.id} value={tab.id}
          >{tab.name}</TabsTrigger>
        ))}
      </TabsList>
      {/* <div className="flex flex-1 flex-col h-full"> */}
      {tabs.map((tab: any) => (
        <TabsContent key={tab.id} value={tab.id} className="h-full">
          {tab.type === "text" ? (
            <TextOnlyTabContent content={tab.content as string} />
          ) :
            tab.type === "image" ? (
              <ImageAndTextTabContent image={tab.content as TabContent as any} content={""} />
            ) :

              (
                typeof tab.content !== 'string' && (
                  <ImageAndTextTabContent image={tab.content.image} content={tab.content.text} />
                )
              )


          }
        </TabsContent>
      ))}
      {/* </div> */}
    </Tabs>
  )
}

const TabsSection = ({ data }: TabsSectionProps) => {
  if (!data || data.length === 0) {
    return null;
  }
  return (
    <div id="pdp-tabs-section" className={
      cn(
        "w-full mt-xl",
        "flex min-h-[30rem] max-h-[50vh] overflow-y-auto",
      )
    }>
      <TabsBuilder data={data} />

    </div>
  )

}

export default TabsSection