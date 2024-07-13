"use server";

import { cn } from "@/lib/utils";

interface RelatedSectionProps {
  product: any;
}

const RelatedSection = ({ product }: RelatedSectionProps) => {

  return (
    <section id="pdp-related-section" className={
      cn("h-[80vh] w-full border-2 border-black")
    }>
      RelatedSection - {product.name || "No product name"}
    </section >
  )
}

export default RelatedSection