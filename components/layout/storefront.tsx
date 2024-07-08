"use client";

import { cn } from "@/lib/utils";
import BasicFooter from "@/template/footer/basic";
import BasicHeader from "@/template/header/basic";
import { useContext } from "react";
import { PreviewContext } from "@/components/preview/context";

const StorefrontLayout = ({ children }: { children: React.ReactNode }) => {
  const { mode } = useContext(PreviewContext);
  return (
    <div className={cn("flex flex-col h-full min-h-screen justify-center items-center self-center mx-auto",
      mode === "phone" ? "max-w-md" : "max-w-full",
      "border-2 border-primary border-dashed z-50"
    )}
    >
      <BasicHeader themeName="coffee" />
      <div className="grow py-2 px-8">
        {children}
      </div>
      <BasicFooter />
    </div>
  )
}

export default StorefrontLayout;