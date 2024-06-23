from utils.base import PyBaseModel


class AddressBase(PyBaseModel):
    # Create request's insensitive fields
    name: str
    line1: str
    line2: str | None
    city: str
    state: str
    country: str
    postal_code: str


class AddressCreate(AddressBase):
    # Create request's sensitive fields
    pass


class Address(AddressBase):
    id: str
