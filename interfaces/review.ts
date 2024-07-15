import { Customer } from "./customer";
import { ObjectType } from "../utils/enum";

enum FeedbackEnum {
  CUSTOMER_SERVICE = "customer_service",
  LOW_QUALITY = "low_quality",
  MISSING_FEATURES = "missing_features",
  TOO_COMPLEX = "too_complex",
  TOO_EXPENSIVE = "too_expensive",
  UNUSED = "unused",
  OTHER = "other",
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
