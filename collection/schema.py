from pydantic import BaseModel

from product.schema import ProductList
from lib.model import PyBaseModel
from lib.object import ObjectType


class CollectionBase(BaseModel):
    name: str
    handle: str
    image_web: str | None = None
    image_mobile: str | None = None


class CollectionCreate(CollectionBase):
    products: list[str] | None = None


class Collection(CollectionBase, PyBaseModel):
    id: str
    object: str = ObjectType.COLLECTION
    products: ProductList


class CollectionList(BaseModel):
    object: str = "list"
    url: str = "/v1/collections"
    has_more: bool
    data: list[Collection] = []


class ProductsUpdate(BaseModel):
    add: list[str] | None = None
    remove: list[str] | None = None


class CollectionUpdate(BaseModel):
    name: str | None = None
    image_web: str | None = None
    image_mobile: str | None = None
    products: ProductsUpdate | None = None


class CollectionDelete(BaseModel):
    id: str
    object: str = ObjectType.COLLECTION
    deleted: bool
