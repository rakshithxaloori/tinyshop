from sqlmodel import Session, select
from sqlalchemy import func

from review.model import Review
from review import schema
from review.utils import pydantify_reviews
from product.model import Product
from lib.session import update_instance


def create_review(
    shop_id: str,
    livemode: bool,
    review: schema.ReviewCreate,
    db: Session,
) -> schema.Review | None:
    try:
        review_data = review.model_dump(exclude={"product"})
        new_review = Review(
            shop_id=shop_id,
            livemode=livemode,
            product_id=review.product,
            **review_data,
        )
        db.add(new_review)

        db.commit()
        db.refresh(new_review)
        # TODO update rating in product
        py_reviews = pydantify_reviews([new_review])
        return py_reviews.pop()
    except Exception as e:
        print("EXCEPTION create_review:", e)
        return None


def update_review(
    shop_id: str,
    livemode: bool,
    review_id: str,
    review: schema.ReviewUpdate,
    db: Session,
) -> schema.Review | None:
    try:
        data = review.model_dump(exclude_none=True)
        results = db.exec(
            select(Review)
            .where(Review.shop_id == shop_id)
            .where(Review.livemode == livemode)
            .where(Review.id == review_id)
        )
        review_ins = results.one()
        update_instance(db, data, review_ins)
        db.commit()
        db.refresh(review_ins)
        py_reviews = pydantify_reviews([review_ins])
        return py_reviews.pop()
    except Exception as e:
        print("EXCEPTION update_review:", e)
        return None


def retrieve_review(
    shop_id: str,
    livemode: bool,
    review_id: str,
    db: Session,
) -> schema.Review | None:
    try:
        results = db.exec(
            select(Review)
            .where(Review.shop_id == shop_id)
            .where(Review.livemode == livemode)
            .where(Review.id == review_id)
        )
        review_ins = results.one()
        py_reviews = pydantify_reviews([review_ins])
        return py_reviews.pop()
    except Exception as e:
        print("EXCEPTION retrieve_review:", e)
        return None


def list_reviews(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.ReviewList:
    try:
        subquery = select(Review.id).offset(skip).limit(limit).subquery()
        results = db.exec(
            select(Review)
            .where(Review.shop_id == shop_id)
            .where(Review.livemode == livemode)
            .where(Review.id.in_(subquery))
        )
        all_rows = list(results.all())
        reviews = pydantify_reviews(all_rows)
        return schema.ReviewList(
            has_more=False,  # TODO
            data=reviews,
        )
    except Exception as e:
        print("EXCEPTION list_reviews:", e)
        return None


def delete_review(
    shop_id: str,
    livemode: bool,
    review_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Review)
            .where(Review.shop_id == shop_id)
            .where(Review.livemode == livemode)
            .where(Review.id == review_id)
        )
        review = results.one()
        db.delete(review)
        db.commit()
        return review.id
    except Exception as e:
        print("EXCEPTION delete_review:", e)
        return None
