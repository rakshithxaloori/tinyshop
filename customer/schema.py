from pydantic import BaseModel

from utils.model import PyBaseModel
from utils.object import object_type
from customer.address.schema import CustomerAddressCreate, CustomerAddressList


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
    object: str = object_type.CUSTOMER
    addresses: CustomerAddressList | None = None


class CustomerList(BaseModel):
    object: str = "list"
    url: str = "/v1/customers"
    has_more: bool
    data: list[Customer] = []


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class CustomerDelete(BaseModel):
    id: str
    object: str = object_type.CUSTOMER
    deleted: bool
