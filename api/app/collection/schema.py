from pydantic import BaseModel

from app.product.schema import ProductList
from app.lib.model import PyBaseModel
from app.lib.object import ObjectType


class CollectionBase(BaseModel):
    name: str
    image_web: str | None = None
    image_mobile: str | None = None


class CollectionCreate(CollectionBase):
    products: list[str] | None = None


class Collection(CollectionBase, PyBaseModel):
    id: str
    object: str = ObjectType.COLLECTION
    handle: str
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
