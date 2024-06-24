from utils.base import PyBaseModel
from customer.addresses.schemas import Address


class CustomerBase(PyBaseModel):
    # Create request's insensitive fields
    name: str
    email: str | None
    phone: str

    address: Address


class CustomerCreate(PyBaseModel):
    # Create request's sensitive fields
    pass


class AddressList(PyBaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[Address] = []


class Customer(PyBaseModel):
    id: str

    addresses: AddressList
