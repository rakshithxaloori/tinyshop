import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { ReviewBlock } from "./review-card";
import { Progress } from "@/components/ui/progress";

const ReviewsRankOverview = ({ reviews }: { reviews: any[] }) => {
  const numReviews = reviews.length;
  // count the number of 1-5 star reviews
  const stars = [0, 0, 0, 0, 0];
  reviews.forEach((review) => {
    stars[review.product_rating - 1]++;
  });
  const avgRating = numReviews === 0 ? 0 : reviews.reduce((acc, review) => acc + review.product_rating, 0) / numReviews;
  return (
    <Card className="border-primary bg-base-100">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          Customer reviews
          <ReviewBlock reviewValue={avgRating} />
        </CardTitle>
        <CardDescription>{numReviews} reviews</CardDescription>
      </CardHeader>
      <CardContent>
        {
          stars.reverse().map((num, index) => (
            <div key={index} className="flex flex-1 gap-2 items-center">
              <div className="flex flex-row items-center  px-2 gap-2">
                {5 - index} star
              </div>
              <div className="flex flex-1 gap-2 items-center">
                <Progress className="w-full fill-primary bg-base-300" value={(num / numReviews) * 100} />
              </div>

            </div>
          ))
        }
      </CardContent>
    </Card>
  )
}

export default ReviewsRankOverview