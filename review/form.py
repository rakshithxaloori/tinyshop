from typing import Annotated
from fastapi import Form


from review import schema
from review.model import FeedbackEnum


def create_review_form(
    product: Annotated[str, Form()],
    customer: Annotated[str, Form()],
    product_rating: Annotated[int, Form()],
    shipping_rating: Annotated[int, Form()],
    feedback: Annotated[FeedbackEnum | None, Form()] = None,
    review: Annotated[str | None, Form()] = None,
) -> schema.ReviewCreate:
    return schema.ReviewCreate(
        customer=customer,
        product=product,
        product_rating=product_rating,
        shipping_rating=shipping_rating,
        feedback=feedback,
        review=review,
    )


def update_review_form(
    product_rating: Annotated[int | None, Form()] = None,
    shipping_rating: Annotated[int | None, Form()] = None,
    feedback: Annotated[FeedbackEnum | None, Form()] = None,
    review: Annotated[str | None, Form()] = None,
) -> schema.ReviewUpdate:
    return schema.ReviewUpdate(
        product_rating=product_rating,
        shipping_rating=shipping_rating,
        feedback=feedback,
        review=review,
    )
