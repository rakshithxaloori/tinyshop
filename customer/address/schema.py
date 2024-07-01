from pydantic import BaseModel

from utils.model import PyBaseModel
from utils.object import object_type


class CustomerAddressBase(BaseModel):
    # Create request's insensitive fields
    name: str
    line1: str
    line2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str


class CustomerAddressCreate(CustomerAddressBase):
    # Create request's sensitive fields
    pass


class CustomerAddress(CustomerAddressBase, PyBaseModel):
    id: str
    object: str = object_type.CUSTOMER_ADDRESS


class CustomerAddressList(BaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[CustomerAddress] = []


class CustomerAddressUpdate(BaseModel):
    name: str | None = None
    line1: str | None = None
    line2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class CustomerAddressDelete(BaseModel):
    id: str
    object: str = object_type.CUSTOMER_ADDRESS
    deleted: bool
