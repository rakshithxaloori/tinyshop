from review.model import Review
from review import schema


def pydantify_reviews(rows: list[Review]) -> list[schema.Review]:
    reviews: list[schema.Review] = []
    for rev in rows:
        reviews.append(
            schema.Review(
                **rev.model_dump(exclude={"created", "updated"}),
                created=int(rev.created.timestamp()),
                updated=int(rev.updated.timestamp()),
            )
        )
    return reviews
