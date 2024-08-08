from pydantic import BaseModel

from app.lib.model import PyBaseModel
from app.lib.object import ObjectType
from app.variant.schema import Variant


class ProductBase(BaseModel):
    # Create request's insensitive fields
    name: str
    description: str | None = None
    images: list[str] | None = None
    active: bool
    shippable: bool
    preorder: bool

    # TODO images max length 20


class ProductCreate(ProductBase):
    pass


class Product(ProductBase, PyBaseModel):
    id: str
    handle: str
    object: str = ObjectType.PRODUCT
    default_variant: Variant | None = None
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
