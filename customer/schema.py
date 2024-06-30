from pydantic import BaseModel

from utils.model import PyBaseModel


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
    object: str = "customer_address"


class AddressList(BaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[CustomerAddress] = []


class CustomerBase(BaseModel):
    # Create request's insensitive fields
    name: str
    email: str | None = None
    phone: str


class CustomerCreate(CustomerBase):
    # Create request's sensitive fields
    address: CustomerAddressCreate | None = None


class Customer(CustomerBase, PyBaseModel):
    id: str
    object: str = "customer"
    addresses: AddressList | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class CustomerDelete(BaseModel):
    id: str
    object: str = "customer"
    deleted: bool
