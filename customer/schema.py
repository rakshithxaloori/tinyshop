from utils.base import PyBaseModel


class CustomerAddressBase(PyBaseModel):
    # Create request's insensitive fields
    name: str
    line1: str
    line2: str | None
    city: str
    state: str
    country: str
    postal_code: str


class CustomerAddressCreate(CustomerAddressBase):
    # Create request's sensitive fields
    pass


class CustomerAddress(CustomerAddressBase):
    id: str


class CustomerBase(PyBaseModel):
    # Create request's insensitive fields
    name: str
    email: str | None
    phone: str

    address: CustomerAddress


class CustomerCreate(PyBaseModel):
    # Create request's sensitive fields
    pass


class AddressList(PyBaseModel):
    object: str = "list"
    url: str
    has_more: bool
    data: list[CustomerAddress] = []


class Customer(PyBaseModel):
    id: str

    addresses: AddressList
