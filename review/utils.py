from review.model import Review
from review import schema
from customer import schema as cus_schema


def pydantify_reviews(rows: list[Review]) -> list[schema.Review]:
    reviews: list[schema.Review] = []
    for rev in rows:
        cus = rev.customer
        reviews.append(
            schema.Review(
                **rev.model_dump(exclude={"customer"}),
                customer=cus_schema.Customer(
                    **cus.model_dump(exclude={"phone", "email"}),
                ),
            )
        )
    return reviews
