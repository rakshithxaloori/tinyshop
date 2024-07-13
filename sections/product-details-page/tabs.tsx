"use server";

import { cn } from "@/lib/utils";
import Image from "next/image";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface TabsSectionProps {
  product: any;
  config: any
}

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ImageAndTextTabContent, TextOnlyTabContent } from "@/template/tab-content/basic";

type TabType = "text" | "text-image"
type TabContent = string | {
  image: {
    src: string
    alt: string
  }
  text: string
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

const TabsBuilder = () => {
  const { defaultTab, tabs } = tabSpec
  const numtabs = tabs.length
  const tailwindClass =
    (numtabs === 2) ? "grid-cols-2" :
      (numtabs === 3) ? "grid-cols-3" :
        (numtabs === 4) ? "grid-cols-4" :
          "grid-cols-1"


  return (
    <Tabs defaultValue={defaultTab}
      className="w-full min-h-full flex flex-1 flex-col border-2 border-primary rounded-lg shadow-sm">
      <TabsList className={
        cn("grid w-full",
          tailwindClass,
        )
      }>
        {tabs.map(tab => (
          <TabsTrigger key={tab.id} value={tab.id}
          >{tab.name}</TabsTrigger>
        ))}
      </TabsList>
      {/* <div className="flex flex-1 flex-col h-full"> */}
      {tabs.map(tab => (
        <TabsContent key={tab.id} value={tab.id} className="h-full">
          {tab.type === "text" ? (
            <TextOnlyTabContent content={tab.content as string} />
          ) : (
            typeof tab.content !== 'string' && (
              <ImageAndTextTabContent image={tab.content.image} content={tab.content.text} />
            )
          )}
        </TabsContent>
      ))}
      {/* </div> */}
    </Tabs>
  )
}

const TabsSection = ({ product, config }: TabsSectionProps) => {

  return (
    <div id="pdp-tabs-section" className={
      cn(
        "w-full mt-xl",
        "flex min-h-[30rem] max-h-[50vh] overflow-y-auto",
      )
    }>
      <TabsBuilder />

    </div>
  )

}

export default TabsSection