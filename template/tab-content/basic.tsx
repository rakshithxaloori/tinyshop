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
      className="grid grid-cols-1 md:grid-cols-2 gap-y-[1rem] p-4 h-full"
    >
      <div className="relative w-1/2 h-full mx-auto ">
        <Image src={src} alt={alt} fill className="rounded-xl" />
      </div>
      <p
      >{content}</p>
    </div>
  )
}

const ImageOnlyTabContent = ({ image }: {
  image: {
    src: string
    alt: string
  }
}) => {
  const { src, alt } = image
  return (
    <div
      className="grid grid-cols-1  gap-y-[1rem] p-4 h-full w-full justify-center"
    >
      <div className="relative w-full h-full mx-auto max-w-screen md:max-w-md lg:max-w-lg">
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