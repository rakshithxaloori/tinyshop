from sqlmodel import Session, select

from customer.model import Customer
from customer import schema
from customer.address.model import CustomerAddress
from customer.utils import pydantify_customers
from database import engine


def create_customer(
    x_shop_id: str,
    livemode: bool,
    customer: schema.CustomerCreate,
) -> schema.Customer | None:
    with Session(engine) as db:
        try:
            customer_data = customer.model_dump(exclude={"address"})
            # TODO make this a transaction
            # Create a customer
            new_customer = Customer(
                shop_id=x_shop_id,
                livemode=livemode,
                **customer_data,
            )
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)

            new_address = None
            if customer.address:
                address_data = customer.address.model_dump()
                new_address = CustomerAddress(
                    livemode=livemode,
                    customer_id=new_customer.id,
                    **address_data,
                )
                db.add(new_address)
                db.commit()
                db.refresh(new_address)
            py_customers = pydantify_customers([(new_customer, new_address)])
            return py_customers.pop()
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
                .where(Customer.livemode == livemode)
                .where(Customer.id == customer_id)
            )
            result = db.exec(statement)
            updated_customer = result.one()

            for key, value in update_data.items():
                setattr(updated_customer, key, value)

            db.add(updated_customer)
            db.commit()
            db.refresh(updated_customer)
            py_customers = pydantify_customers([(updated_customer, None)])
            return py_customers.pop()
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
                .where(Customer.livemode == livemode)
                .where(Customer.id == id)
                .where(Customer.id == CustomerAddress.customer_id)
            )
            all_rows = list(results.all())
            py_customers = pydantify_customers(all_rows)
            return py_customers.pop()

        except Exception as e:
            print("EXCEPTION retrieve_customer:", e)
            return None


def list_customers(
    x_shop_id: str,
    livemode: bool,
    skip: str = None,
    limit: int = 50,
) -> schema.CustomerList:
    with Session(engine) as db:
        # TODO skip and limit
        subquery = select(Customer.id).offset(skip).limit(limit).subquery()

        results = db.exec(
            select(Customer, CustomerAddress)
            .where(Customer.shop_id == x_shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id.in_(subquery))
            .where(Customer.id == CustomerAddress.customer_id)
        )
        all_rows = list(results.all())
        customers = pydantify_customers(all_rows)
        return schema.CustomerList(
            has_more=False,  # TODO here and in addresses router
            data=customers,
        )


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
                .where(Customer.livemode == livemode)
                .where(Customer.id == id)
            )
            customer = results.one()
            db.delete(customer)
            db.commit()
            return customer.id
        except Exception as e:
            print("EXCEPTION delete_customer:", e)
            return None
