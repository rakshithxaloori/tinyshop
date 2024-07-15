from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from review.model import FeedbackEnum
from customer.schema import Customer


class ReviewBase(BaseModel):
    product_rating: int
    shipping_rating: int
    feedback: FeedbackEnum | None = None
    review: str | None = None
    image: str | None = None


class ReviewCreate(ReviewBase):
    customer: str
    product: str


class Review(ReviewBase, PyBaseModel):
    id: str
    object: str = ObjectType.REVIEW
    customer: Customer


class ReviewList(BaseModel):
    object: str = "list"
    url: str = "/v1/reviews"
    has_more: bool
    data: list[Review] = []


class ReviewUpdate(BaseModel):
    product_rating: int | None
    shipping_rating: int | None
    feedback: FeedbackEnum | None = None
    review: str | None = None


class ReviewDelete(BaseModel):
    id: str
    object: str = ObjectType.REVIEW
    deleted: bool
