from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from customer_address.schema import CustomerAddressList


class CustomerBase(BaseModel):
    # Create request's insensitive fields
    name: str | None = None


class CustomerCreate(CustomerBase):
    # Create request's sensitive fields
    email: str | None = None
    phone: str
    send_otp: bool = False


class Customer(CustomerBase, PyBaseModel):
    id: str
    object: str = ObjectType.CUSTOMER
    is_verified: bool
    email: str | None = None
    phone: str | None = None
    addresses: CustomerAddressList | None = None


class CustomerList(BaseModel):
    object: str = "list"
    url: str = "/v1/customers"
    has_more: bool
    data: list[Customer] = []


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    otp: str | None = None
    send_otp: bool = False


class CustomerDelete(BaseModel):
    id: str
    object: str = ObjectType.CUSTOMER
    deleted: bool
