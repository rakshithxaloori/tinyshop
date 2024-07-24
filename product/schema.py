from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from option.schema import OptionList
from variant.schema import VariantList, Variant


class CollectionBase(BaseModel):
    name: str
    image_web: str | None = None
    image_mobile: str | None = None


class Collection(CollectionBase, PyBaseModel):
    id: str
    object: str = ObjectType.COLLECTION
    handle: str


class CollectionList(BaseModel):
    object: str = "list"
    url: str = "/v1/collections"
    has_more: bool
    data: list[Collection] = []


class ProductBase(BaseModel):
    # Create request's insensitive fields
    name: str
    description: str | None = None
    images: list[str] | None = None
    active: bool
    shippable: bool
    preorder: bool


class ProductCreate(ProductBase):
    pass


class Product(ProductBase, PyBaseModel):
    id: str
    handle: str
    object: str = ObjectType.PRODUCT
    default_variant: Variant | None = None
    options: OptionList | None = None
    variants: VariantList | None = None
    collections: CollectionList | None = None
    rating: int | None = None


class ProductList(BaseModel):
    object: str = "list"
    url: str = "/v1/products"
    has_more: bool
    data: list[Product] | list[str] = []


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    shippable: bool | None = None
    preorder: bool | None = None


class ProductDelete(BaseModel):
    id: str
    object: str = ObjectType.PRODUCT
    deleted: bool
