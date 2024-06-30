from customer.model import Customer, CustomerAddress
from customer.schema import (
    Customer as PyCustomer,
    CustomerAddress as PyCustomerAddress,
    AddressList as PyAddressList,
)


def pydantify_customers(
    rows: list[tuple[Customer, CustomerAddress | None]]
) -> list[PyCustomer]:
    customers_dict = {}
    for customer, address in rows:
        if customer.id not in customers_dict:
            customers_dict[customer.id] = PyCustomer(
                id=customer.id,
                email=customer.email,
                name=customer.name,
                phone=customer.phone,
                created=int(customer.created.timestamp()),
                updated=int(customer.updated.timestamp()),
                livemode=customer.livemode,
                addresses=PyAddressList(
                    data=[],
                    has_more=False,  # TODO has_more
                    url="v1/customers/{customer_id}/addresses".format(
                        customer_id=customer.id
                    ),
                ),
            )
        if address:
            customers_dict[customer.id].addresses.data.append(
                PyCustomerAddress(
                    id=address.id,
                    name=address.name,
                    line1=address.line1,
                    line2=address.line2,
                    city=address.city,
                    state=address.state,
                    postal_code=address.postal_code,
                    country=address.country,
                    created=int(address.created.timestamp()),
                    updated=int(address.updated.timestamp()),
                    livemode=address.livemode,
                )
            )

    return list(customers_dict.values())
