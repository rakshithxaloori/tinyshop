from sqlmodel import Session, select

from customer.model import Customer, CustomerAddress
from customer import schema

from customer.utils import pydantify_customers
from database import engine


def create_customer(
    x_shop_id: str,
    livemode: bool,
    customer: schema.CustomerCreate,
) -> schema.Customer:
    with Session(engine) as db:
        try:
            # Create a customer
            new_customer = Customer(
                livemode=livemode,
                name=customer.name,
                phone=customer.phone,
                email=customer.email,
                shop_id=x_shop_id,
            )
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)

            new_address = None
            if customer.address:
                address = customer.address
                new_address = CustomerAddress(
                    livemode=livemode,
                    name=address.name,
                    line1=address.line1,
                    line2=address.line2,
                    city=address.city,
                    state=address.state,
                    country=address.country,
                    postal_code=address.postal_code,
                    customer_id=new_customer.id,
                )
                db.add(new_address)
                db.commit()
                db.refresh(new_address)
            py_customers = pydantify_customers([(new_customer, new_address)])
            return py_customers.pop() if len(py_customers) >= 1 else None
        except Exception as e:
            print("EXCEPTION create_customer:", e)
            return None


def update_customer(
    x_shop_id: str,
    livemode: bool,
    customer_id: str,
    customer: schema.CustomerUpdate,
) -> schema.Customer | None:
    with Session(engine) as db:
        try:
            update_data = customer.model_dump(exclude_none=True)

            statement = (
                select(Customer)
                .where(Customer.shop_id == x_shop_id)
                .where(Customer.id == customer_id)
                .where(Customer.livemode == livemode)
            )
            result = db.exec(statement)
            updated_customer = result.one()

            for key, value in update_data.items():
                setattr(updated_customer, key, value)

            db.add(updated_customer)
            db.commit()
            db.refresh(updated_customer)
            py_customers = pydantify_customers([(updated_customer, None)])
            return py_customers.pop() if len(py_customers) >= 1 else None
        except Exception as e:
            # TODO create
            print("EXCEPTION update_customer:", e)
            return None


def retrieve_customer(
    x_shop_id: str,
    livemode: bool,
    id: str,
) -> schema.Customer | None:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(Customer, CustomerAddress)
                .where(Customer.shop_id == x_shop_id)
                .where(Customer.id == id)
                .where(Customer.id == CustomerAddress.customer_id)
                .where(Customer.livemode == livemode)
            )
            all_rows = list(results.all())
            py_customers = pydantify_customers(all_rows)
            return py_customers.pop() if len(py_customers) >= 1 else None

        except Exception as e:
            print("EXCEPTION retrieve_customer:", e)
            return None


def list_customers(
    x_shop_id: str,
    livemode: bool,
    skip: str = None,
    limit: int = 50,
) -> list[schema.Customer]:
    with Session(engine) as db:
        subquery = select(Customer.id).offset(skip).limit(limit).subquery()

        results = db.exec(
            select(Customer, CustomerAddress)
            .where(Customer.shop_id == x_shop_id)
            .where(Customer.id.in_(subquery))
            .where(Customer.id == CustomerAddress.customer_id)
            .where(Customer.livemode == livemode)
        )
        all_rows = list(results.all())
        return pydantify_customers(all_rows)


def delete_customer(
    x_shop_id: str,
    livemode: bool,
    id: str,
) -> str | None:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(Customer)
                .where(Customer.shop_id == x_shop_id)
                .where(Customer.id == id)
                .where(Customer.livemode == livemode)
            )
            customer = results.one()
            db.delete(customer)
            db.commit()
            return customer.id
        except Exception as e:
            print("EXCEPTION delete_customer:", e)
            return None
