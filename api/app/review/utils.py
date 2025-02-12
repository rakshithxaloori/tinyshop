from app.review.model import Review
from app.review import schema
from app.customer.utils import pydantify_customers


def pydantify_reviews(rows: list[Review]) -> list[schema.Review]:
    reviews: list[schema.Review] = []
    for rev in rows:
        cus = rev.customer
        reviews.append(
            schema.Review(
                **rev.model_dump(exclude={"customer"}),
                customer=pydantify_customers([cus]).pop(),
            )
        )
    return reviews
