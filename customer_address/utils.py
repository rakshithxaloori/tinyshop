from user_address.model import UserAddress
from customer_address.schema import CustomerAddress as PyCustomerAddress


def pydantify_addresses(rows: list[UserAddress]) -> list[PyCustomerAddress]:
    addresses: list[PyCustomerAddress] = []
    for address in rows:
        addresses.append(
            PyCustomerAddress(
                **address.model_dump(exclude={"id"}),
                id=address.id,
            )
        )
    return addresses
