from customer.model import Customer
from customer import schema
from customer_address import schema as ca_schema


from lib.limit import LIST_LIMIT_COUNT


def pydantify_customers(rows: list[Customer]) -> list[schema.Customer]:
    customers: list[schema.Customer] = []
    for customer in rows:
        customers.append(
            schema.Customer(
                **customer.user.model_dump(exclude={"id", "addresses"}),
                id=customer.id,
                addresses=ca_schema.CustomerAddressList(
                    data=[
                        ca_schema.CustomerAddress(**addr.model_dump())
                        for addr in customer.user.addresses[:LIST_LIMIT_COUNT]
                    ],
                    has_more=False,  # TODO has_more
                    url="/v1/customers/{customer_id}/addresses".format(
                        customer_id=customer.id
                    ),
                ),
            )
        )

    return customers
