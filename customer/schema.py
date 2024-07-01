from pydantic import BaseModel

from utils.model import PyBaseModel
from customer.address.schema import CustomerAddressCreate, CustomerAddressList


OBJECT_STR = "customer"


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
    object: str = OBJECT_STR
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
    object: str = OBJECT_STR
    deleted: bool
