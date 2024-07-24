from customer_address.model import CustomerAddress
from customer_address.schema import CustomerAddress as PyCustomerAddress


def pydantify_addresses(rows: list[CustomerAddress]) -> list[PyCustomerAddress]:
    addresses: list[PyCustomerAddress] = []
    for address in rows:
        addresses.append(
            PyCustomerAddress(
                **address.model_dump(),
            )
        )
    return addresses
