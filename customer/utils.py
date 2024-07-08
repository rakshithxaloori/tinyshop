from customer.model import Customer
from customer import schema
from customer_address.model import CustomerAddress
from customer_address import schema as ca_schema


def pydantify_customers(
    rows: list[tuple[Customer, CustomerAddress | None]]
) -> list[schema.Customer]:
    customers_dict: dict[str, schema.Customer] = {}
    for customer, address in rows:
        if customer.id not in customers_dict:
            customers_dict[customer.id] = schema.Customer(
                **customer.model_dump(exclude={"created", "updated"}),
                created=int(customer.created.timestamp()),
                updated=int(customer.updated.timestamp()),
                addresses=ca_schema.CustomerAddressList(
                    data=[],
                    has_more=False,  # TODO has_more
                    url="/v1/customers/{customer_id}/addresses".format(
                        customer_id=customer.id
                    ),
                ),
            )
        if address:
            customers_dict[customer.id].addresses.data.append(
                ca_schema.CustomerAddress(
                    **address.model_dump(exclude={"created", "updated"}),
                    created=int(address.created.timestamp()),
                    updated=int(address.updated.timestamp()),
                )
            )

    return list(customers_dict.values())
