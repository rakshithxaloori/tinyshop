import random
from customer.model import Customer
from customer import schema
from customer_address import schema as ca_schema


from lib.limit import LIST_LIMIT_COUNT


def pydantify_customers(rows: list[Customer]) -> list[schema.Customer]:
    customers: list[schema.Customer] = []
    for customer in rows:
        if customer.is_verified:
            customers.append(
                schema.Customer(
                    **customer.user.model_dump(
                        exclude={"id", "addresses", "created", "updated", "livemode"}
                    ),
                    **customer.model_dump(exclude={"otp"}),
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
        else:
            customers.append(
                schema.Customer(
                    phone=customer.user.phone,
                    **customer.model_dump(exclude={"otp"}),
                )
            )

    return customers


def send_otp(phone: str) -> str:
    random_number = "".join([str(random.randint(0, 9)) for _ in range(6)])
    print("----------------------------")
    # TODO delete this
    print("OTP", random_number)
    print("----------------------------")
    return random_number
