from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import object_type


class ProductBase(BaseModel):
    # Create request's insensitive fields
    name: str
    description: str | None = None
    images: list[str] | None = None
    active: bool
    shippable: bool
    preorder: bool


class ProductCreate(ProductBase):
    handle: str


class Product(ProductBase, PyBaseModel):
    id: str
    handle: str
    object: str = object_type.PRODUCT


class ProductList(BaseModel):
    object: str = "list"
    url: str = "/v1/products"
    has_more: bool
    data: list[Product] = []


class ProductUpdate(BaseModel):
    name: str | None = None
    handle: str | None = None
    description: str | None = None
    active: bool | None = None
    shippable: bool | None = None
    preorder: bool | None = None


class ProductDelete(BaseModel):
    id: str
    object: str = object_type.PRODUCT
    deleted: bool
