"use server";

import { cn } from "@/lib/utils";

interface ReviewsSectionProps {
  product: any;
  className?: string;
}

const ReviewsSection = (props: ReviewsSectionProps) => {
  const {
    product,
    className
  } = props;

  return (
    <section id="pdp-reviews-section" className={
      cn("h-[80vh] w-full", className)
    }>
      ReviewsSection
    </section >
  )

}

export default ReviewsSection