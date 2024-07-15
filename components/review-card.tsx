"use client"
import { cn } from "@/lib/utils";
import Avatar, { genConfig } from 'react-nice-avatar'
import { Badge } from "./ui/badge";


type TReview = {
  feedback: string;
  product_rating: number;
  shipping_rating: number;
  name: string;
  review: string;
  customer: {
    name: string;
  };
}

function toCamelCase(str: string): string {
  return str.replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) =>
    index === 0 ? word.toLowerCase() : word.toUpperCase()
  ).replace(/\s+/g, '');
}

function toTitleCase(str: string): string {
  return str.replace(
    /\w\S*/g,
    (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  );
}

export const ReviewBlock = ({ reviewValue }: { reviewValue: number }) => {
  const badgeColor = reviewValue >= 4 ? "bg-green-900" :
    reviewValue >= 3 ? "bg-green-400 text-stone-900" :
      reviewValue >= 2 ? "bg-yellow-500" :
        reviewValue >= 1 ? "bg-red-500" : "bg-gray-500";

  return (
    <Badge variant="outline" className={`badge text-xs md:text:sm text-white ${badgeColor} `}>{reviewValue.toFixed(1)}</Badge>
  );
}

const ReviewCard = ({
  review,
  className
}: { review: TReview; className?: string }) => {
  const { name: customerName } = review.customer
  const formattedName = customerName.split('-').slice(0, 2).join(' ')
  const formattedFeedback = review.feedback.split('_').join(' ')
  const { product_rating: productRating, shipping_rating: shippingRating } = review

  const config = genConfig(customerName)

  return (
    <div className={cn("card card-bordered card-compact	bg-base-100 border-2 border-primary",
      className
    )}>
      <div className="card-body gap-0">
        {/* Review card */}
        <h2 className="card-title py-0 my-sm">{toTitleCase(formattedFeedback)}</h2>
        <div className="grid grid-cols-1 gap-1 mb-sm">
          <div className="flex gap-2 justify-between items-center">
            <span className="font-semibold text-base-content/80">Product {" "}</span>
            <ReviewBlock reviewValue={productRating} />
          </div>

          <div className="flex gap-2 justify-between items-center">
            <span className="font-semibold text-base-content/80">Shipping {" "}</span>
            <ReviewBlock reviewValue={shippingRating} />
          </div>

        </div>
        <p className="mb-md" >{review.review}</p>
        <div className="card-footer flex flex-row items-center gap-2">
          <Avatar className="flex-none w-6 h-6" {...config} />
          <p className="text-sm">{toTitleCase(formattedName)}</p>
        </div>


      </div>
      {/* <p>
        {JSON.stringify(review)}
      </p> */}

    </div>
  );
}

export default ReviewCard;