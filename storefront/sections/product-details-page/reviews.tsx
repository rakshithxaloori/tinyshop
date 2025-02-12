import ReviewsRankOverview from "@/components/review-rank";
import { cn } from "@/lib/utils";
import dynamic from "next/dynamic";

const NoSSRReviewCard = dynamic(() => import("@/components/review-card"), { ssr: false })


interface ReviewsSectionProps {
  reviews: any[];
  config: {
    title: string;
  }
}

const ReviewsSection = (props: ReviewsSectionProps) => {
  const {
    reviews,
    config
  } = props;
  const { title } = config;

  let row = 0;

  return (
    <section id="pdp-reviews-section"
      className={cn("my-lg h-full w-full", "scroll-mt-60 md:scroll-mt-40")}>
      <h1 className="text-3xl mb-lg font-bold text-center">{title}</h1>
      <ReviewsRankOverview reviews={reviews} />
      <div className="mt-lg grid grid-subgrid grid-rows-3 grid-col-2 md:grid-cols-3 gap-3 grid-flow-dense">
        {
          reviews.map((review, index) => {

            if (index % 3 === 2) {
              row++;
            }
            // if row is odd, have 3 elements in the row
            // if row is even, have 2 elements in the row

            const twClass = row % 2 === 1 ?
              (index % 2 === 0 ? "col-span-2" : "col-span-1")
              : "col-span-1";

            return (
              <NoSSRReviewCard key={index} review={review}
                className={
                  twClass
                }
              />
            )
          })
        }
      </div>
    </section >
  )

}

export default ReviewsSection