"use client";

import { cn } from "@/lib/utils";
import BasicFooter from "@/template/footer/basic";
import BasicHeader from "@/template/header/basic";

const StorefrontLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className={cn("flex flex-col h-full min-h-screen justify-center items-center self-center mx-auto",
      "bg-base-100",
    )}
      data-theme="retro"
    >
      <BasicHeader />
      <div className="grow w-full h-full">
        {children}
      </div>
      <BasicFooter />
    </div>
  )
}

export default StorefrontLayout;