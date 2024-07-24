from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query


from collection import schema, crud
from lib.dependencies import ShopIDDep, LivemodeDep, FormDep
from lib.session import get_session


router = APIRouter(prefix="/v1/collections")


@router.post("", response_model=schema.Collection)
def create_collection(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    collection: schema.CollectionCreate = FormDep(schema.CollectionCreate),
    db: Session = Depends(get_session),
):
    new_collection = crud.create_collection(
        shop_id,
        livemode,
        collection,
        db,
    )
    return new_collection


@router.post("/{collection_id}", response_model=schema.Collection)
def update_collection(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    collection_id: str,
    collection: schema.CollectionUpdate = FormDep(schema.CollectionUpdate),
    db: Session = Depends(get_session),
):
    collection = crud.update_collection(
        shop_id,
        livemode,
        collection_id,
        collection,
        db,
    )
    return collection


@router.get("/search", response_model=schema.CollectionList)
def search_collections(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    query: Annotated[str, Query()],
    expand: Annotated[list[str] | None, Query(alias="expand[]")] = None,
    db: Session = Depends(get_session),
):
    collections_list = crud.search_collections(
        shop_id,
        livemode,
        query,
        db,
        expand,
    )
    return collections_list


@router.get("/{collection_id}", response_model=schema.Collection)
def retrieve_collection(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    collection_id: str,
    expand: Annotated[list[str] | None, Query(alias="expand[]")] = None,
    db: Session = Depends(get_session),
):
    # TODO expand
    collection = crud.retrieve_collection(
        shop_id,
        livemode,
        collection_id,
        db,
    )
    return collection


@router.get("", response_model=schema.CollectionList)
def list_collections(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    product: Annotated[str | None, Query()] = None,
    expand: Annotated[list[str] | None, Query(alias="expand[]")] = None,
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    collections_list = crud.list_collections(
        shop_id,
        livemode,
        db,
        expand,
        product,
    )
    return collections_list


@router.delete("/{collection_id}", response_model=schema.CollectionDelete)
def delete_collection(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    collection_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_collection(
        shop_id,
        livemode,
        collection_id,
        db,
    )
    return schema.CollectionDelete(
        id=collection_id,
        deleted=deleted_id is not None,
    )
