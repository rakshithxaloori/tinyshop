import random
from app.customer.model import Customer
from app.customer import schema


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
                )
            )
        else:
            customers.append(
                schema.Customer(
                    phone=customer.user.phone,
                    **customer.model_dump(exclude={"otp", "name", "email"}),
                )
            )

    return customers


def send_otp(livemode: bool, phone: str) -> str:
    # TODO implement this
    if not livemode:
        return "000000"
    random_number = "".join([str(random.randint(0, 9)) for _ in range(6)])
    print("----------------------------")
    # TODO delete this
    print("OTP", random_number)
    print("----------------------------")
    return random_number
