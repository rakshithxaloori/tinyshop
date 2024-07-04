from customer.model import Customer
from customer.schema import (
    Customer as PyCustomer,
    CustomerAddressList as PyAddressList,
)
from customer_address.model import CustomerAddress
from customer_address.schema import CustomerAddress as PyCustomerAddress


def pydantify_customers(
    rows: list[tuple[Customer, CustomerAddress | None]]
) -> list[PyCustomer]:
    customers_dict: dict[str, PyCustomer] = {}
    for customer, address in rows:
        if customer.id not in customers_dict:
            customers_dict[customer.id] = PyCustomer(
                **customer.model_dump(exclude={"created", "updated"}),
                created=int(customer.created.timestamp()),
                updated=int(customer.updated.timestamp()),
                addresses=PyAddressList(
                    data=[],
                    has_more=False,  # TODO has_more
                    url="/v1/customers/{customer_id}/addresses".format(
                        customer_id=customer.id
                    ),
                ),
            )
        if address:
            customers_dict[customer.id].addresses.data.append(
                PyCustomerAddress(
                    **address.model_dump(exclude={"created", "updated"}),
                    created=int(address.created.timestamp()),
                    updated=int(address.updated.timestamp()),
                )
            )

    return list(customers_dict.values())
