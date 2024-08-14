import { Customer } from "./customer";
import { ObjectType } from "../utils/enum";

enum FeedbackEnum {
  // Negative feedback
  LOW_QUALITY = "low_quality",
  TOO_EXPENSIVE = "too_expensive",
  OTHER = "other",

  // Positive feedback
  HIGH_QUALITY = "high_quality",
  EASY_TO_USE = "easy_to_use",
  GOOD_VALUE = "good_value",

  // Neutral feedback
  SATISFACTORY = "satisfactory",
  AVERAGE = "average",
}

interface ReviewBase {
  product_rating: number;
  shipping_rating: number;
  feedback?: FeedbackEnum | null;
  review?: string | null;
}

interface ReviewCreate extends ReviewBase {
  customer: string;
  product: string;
}

interface Review extends ReviewBase {
  id: string;
  object: typeof ObjectType.REVIEW;
  customer: Customer;
}

interface ReviewList {
  object: string;
  url: string;
  has_more: boolean;
  data: Review[];
}

interface ReviewUpdate {
  product_rating?: number;
  shipping_rating?: number;
  feedback?: FeedbackEnum | null;
  review?: string | null;
}

interface ReviewDelete {
  id: string;
  object: typeof ObjectType.REVIEW;
  deleted: boolean;
}

export type { Review, ReviewCreate, ReviewUpdate, ReviewList, ReviewDelete };

export { FeedbackEnum };
