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
    <div
      className="grid grid-cols-2 gap-y-[1rem] p-4 h-full"
    >
      <div className="relative w-1/2 h-full aspect-square mx-auto ">
        <Image src={src} alt={alt} fill className="rounded-xl" />
      </div>
      <p>{content}</p>
    </div>
  )
}

const ImageOnlyTabContent = ({ image, className }: {
  image: {
    src: string
    alt: string
  },
  className?: string
}) => {
  const { src, alt } = image
  return (
    <div
      className={cn("grid grid-cols-1 gap-y-[1rem] p-4 h-full border-2 border-primary",
        className
      )}
    >
      <div className="relative w-3/4 h-full mx-auto ">
        <Image src={src} alt={alt} fill className="rounded-xl" />
      </div>
    </div>
  )
}


export {
  TextOnlyTabContent,
  ImageOnlyTabContent,
  ImageAndTextTabContent
}