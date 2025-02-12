from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query


from app.review import schema, crud
from app.lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from app.lib.session import get_session


router = APIRouter(prefix="/v1/reviews")


@router.post("", response_model=schema.Review)
def create_review(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    review: schema.ReviewCreate = FormDep(schema.ReviewCreate),
    db: Session = Depends(get_session),
):
    new_review = crud.create_review(
        shop_id,
        livemode,
        review,
        db,
    )
    return new_review


@router.post("/{review_id}", response_model=schema.Review | None)
def update_review(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    review_id: str,
    review: schema.ReviewUpdate = FormDep(schema.ReviewUpdate),
    db: Session = Depends(get_session),
):
    review = crud.update_review(
        shop_id,
        livemode,
        review_id,
        review,
        db,
    )
    return review


@router.get("/{review_id}", response_model=schema.Review)
def retrieve_review(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    review_id: str,
    db: Session = Depends(get_session),
):
    review = crud.retrieve_review(
        shop_id,
        livemode,
        review_id,
        db,
    )
    return review


@router.get("", response_model=schema.ReviewList)
def list_reviews(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product_id: Annotated[str | None, Query(alias="product")] = None,
    customer_id: Annotated[str | None, Query(alias="customer")] = None,
    db: Session = Depends(get_session),
):
    if product_id is None and customer_id is None:
        # TODO raise error
        pass
    # TODO both product_id and customer_id can't be given at the same time - XOR validation

    # TODO skip limit
    reviews_list = crud.list_reviews(
        shop_id,
        livemode,
        product_id,
        customer_id,
        db,
    )
    return reviews_list


@router.delete("/{review_id}", response_model=schema.ReviewDelete)
def delete_review(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    review_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_review(
        shop_id,
        livemode,
        review_id,
        db,
    )
    return schema.ReviewDelete(
        id=review_id,
        deleted=deleted_id is not None,
    )
