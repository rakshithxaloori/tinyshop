"use server";
import Image from "next/image"
import Link from "next/link";

interface Basic2DHeroSectionProps {
  config: {
    title: string
    description: string
    cta: {
      text: string
      url: string
    }
    image: {
      src: string
      alt: string
    }
  }
}

const Basic2DHeroSection = ({ config }: Basic2DHeroSectionProps) => {
  const { title, description, cta, image } = config
  return (
    <section className="rounded-lg bg-base-100 py-8 sm:py-12 md-lg md:my-xl">
      <div className="mx-auto grid grid-cols-1 items-center justify-items-center gap-8 md:grid-cols-2">
        <div className="space-y-4 w-full">
          <h2 className="text-base-content text-3xl font-bold tracking-tight md:text-4xl">
            {title}
          </h2>
          <p className="text-pretty text-base-content/80">
            {description}
          </p>
          <Link
            className="btn btn-wide
            bg-primary
            text-primary-content
            hover:bg-primary/90
            rounded-lg 
            hover:text-opacity-100
            hover:border-secondary"
            href={cta.url}>
            {cta.text}
          </Link>
        </div>
        <div className="relative min-h-[50dvh] w-full max-sm:mt-lg">
          <Image
            alt={image.alt}
            className="rounded-lg object-cover"
            fill
            src={image.src}
          />
        </div>
      </div>
    </section>
  )
}

export default Basic2DHeroSection