"use server";

import { cn } from "@/lib/utils";
import Image from "next/image";

const TextOnlyTabContent = ({ content }: {
  content: string
}) => {
  return (
    <div className={cn("p-4")}>
      {content}
    </div>
  )
}

const ImageAndTextTabContent = ({ image, content }: {
  image: {
    src: string
    alt: string
  }
  content: string
}) => {
  const { src, alt } = image
  return (
    <div className={cn("flex flex-row flex-1 p-4 h-full",
      "rounded-md justify-between",
    )}>
      <div className="relative w-1/2 h-full ">
        <Image src={src} alt={alt} fill />
      </div>
      <p>{content}</p>
    </div>
  )
}



export {
  TextOnlyTabContent,
  ImageAndTextTabContent
}