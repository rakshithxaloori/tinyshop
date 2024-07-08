from sqlmodel import Session, select
from sqlalchemy.orm import joinedload

from customer.model import Customer
from customer import schema
from customer_address.model import CustomerAddress
from customer.utils import pydantify_customers
from lib.session import update_instance


def create_customer(
    shop_id: str,
    livemode: bool,
    customer: schema.CustomerCreate,
    db: Session,
) -> schema.Customer | None:
    try:
        customer_data = customer.model_dump(exclude={"address"})
        # TODO make this a transaction
        # Create a customer
        new_customer = Customer(
            shop_id=shop_id,
            livemode=livemode,
            **customer_data,
        )
        db.add(new_customer)

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
        db.refresh(new_customer)
        if new_address:
            db.refresh(new_address)

        py_customers = pydantify_customers([(new_customer, new_address)])
        return py_customers.pop()
    except Exception as e:
        print("EXCEPTION create_customer:", e)
        return None


def update_customer(
    shop_id: str,
    livemode: bool,
    customer_id: str,
    customer: schema.CustomerUpdate,
    db: Session,
) -> schema.Customer | None:
    try:
        data = customer.model_dump(exclude_none=True)

        statement = (
            select(Customer)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == customer_id)
        )
        result = db.exec(statement)
        cus_ins = result.one()

        update_instance(db, data, cus_ins)
        db.commit()
        db.refresh(cus_ins)
        py_customers = pydantify_customers([(cus_ins, None)])
        return py_customers.pop()
    except Exception as e:
        # TODO create
        print("EXCEPTION update_customer:", e)
        return None


def retrieve_customer(
    shop_id: str,
    livemode: bool,
    customer_id: str,
    db: Session,
) -> schema.Customer | None:
    try:
        results = db.exec(
            select(Customer, CustomerAddress)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == customer_id)
            .outerjoin(CustomerAddress, Customer.addresses)
            .options(joinedload(Customer.addresses))
        )
        all_rows = list(results.all())
        py_customers = pydantify_customers(all_rows)
        return py_customers.pop()

    except Exception as e:
        print("EXCEPTION retrieve_customer:", e)
        return None


def list_customers(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.CustomerList:
    # TODO skip and limit
    subquery = select(Customer.id).offset(skip).limit(limit).subquery()

    results = db.exec(
        select(Customer, CustomerAddress)
        .where(Customer.shop_id == shop_id)
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
    shop_id: str,
    livemode: bool,
    customer_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Customer)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == customer_id)
        )
        customer = results.one()
        db.delete(customer)
        db.commit()
        return customer.id
    except Exception as e:
        print("EXCEPTION delete_customer:", e)
        return None
