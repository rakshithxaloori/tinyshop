from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from review import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/reviews")


@router.post("", response_model=schema.Review)
def create_review(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    review: Annotated[schema.ReviewCreate, Depends(form.create_review_form)],
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
    review: Annotated[schema.ReviewUpdate, Depends(form.update_review_form)],
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
    db: Session = Depends(get_session),
):
    # TODO skip limit
    reviews_list = crud.list_reviews(
        shop_id,
        livemode,
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
