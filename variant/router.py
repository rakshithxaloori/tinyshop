from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query


from variant import schema, crud
from lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from lib.session import get_session

router = APIRouter(prefix="/v1/variants")


@router.post("", response_model=schema.Variant)
def create_variant(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    variant: schema.VariantCreate = FormDep(schema.VariantCreate),
    db: Session = Depends(get_session),
):
    new_variant = crud.create_variant(
        shop_id,
        livemode,
        variant,
        db,
    )
    return new_variant


@router.post("/{variant_id}", response_model=schema.Variant)
def update_variant(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    variant_id: str,
    variant: schema.VariantUpdate = FormDep(schema.VariantUpdate),
    db: Session = Depends(get_session),
):
    variant = crud.update_variant(
        shop_id,
        livemode,
        variant_id,
        variant,
        db,
    )
    return variant


@router.get("/{variant_id}", response_model=schema.Variant)
def retrieve_variant(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    variant_id: str,
    db: Session = Depends(get_session),
):
    variant = crud.retrieve_variant(
        shop_id,
        livemode,
        variant_id,
        db,
    )
    return variant


@router.get("", response_model=schema.VariantList)
def list_variants(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product: Annotated[str, Query()],
    db: Session = Depends(get_session),
):
    variant_list = crud.list_variants(
        shop_id,
        livemode,
        product,
        db,
    )
    return variant_list


@router.delete("/{variant_id}", response_model=schema.VariantDelete)
def delete_variant(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    variant_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_variant(
        shop_id,
        livemode,
        variant_id,
        db,
    )
    deleted_variant = schema.VariantDelete(
        id=variant_id,
        deleted=deleted_id is not None,
    )
    return deleted_variant
