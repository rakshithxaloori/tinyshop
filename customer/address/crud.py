from sqlmodel import Session, select

from customer.model import Customer
from customer.address.model import CustomerAddress
from customer.address import schema
from customer.address.utils import pydantify_addresses
from database import engine


def create_address(
    x_shop_id: str,
    livemode: bool,
    customer_id: str,
    address: schema.CustomerAddressCreate,
) -> schema.CustomerAddress | None:
    with Session(engine) as db:
        try:
            cus_result = db.exec(
                select(Customer)
                .where(Customer.shop_id == x_shop_id)
                .where(Customer.livemode == livemode)
                .where(Customer.id == customer_id)
            )
            customer = cus_result.one()
            address_data = address.model_dump()
            # Create the address
            new_address = CustomerAddress(
                shop_id=x_shop_id,
                livemode=livemode,
                customer_id=customer.id,
                **address_data,
            )
            db.add(new_address)
            db.commit()
            db.refresh(new_address)
            py_addresses = pydantify_addresses([new_address])
            return py_addresses.pop()
        except Exception as e:
            print("EXCEPTION create_address:", e)
            return None


def update_address(
    x_shop_id: str,
    livemode: bool,
    customer_id: str,
    address_id: str,
    address: schema.CustomerAddressUpdate,
):
    with Session(engine) as db:
        try:
            update_data = address.model_dump(exclude_none=True)

            statement = (
                select(CustomerAddress)
                .where(CustomerAddress.shop_id == x_shop_id)
                .where(CustomerAddress.livemode == livemode)
                .where(CustomerAddress.customer_id == customer_id)
                .where(CustomerAddress.id == address_id)
            )
            result = db.exec(statement)
            updated_address = result.one()

            for key, value in update_data.items():
                setattr(updated_address, key, value)

            db.add(updated_address)
            db.commit()
            db.refresh(updated_address)
            py_addresses = pydantify_addresses([updated_address])
            return py_addresses.pop()
        except Exception as e:
            print("EXCEPTION update_address:", e)
            return None


def retrieve_customer(
    x_shop_id: str,
    livemode: bool,
    customer_id: str,
    address_id: str,
) -> schema.CustomerAddress | None:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(CustomerAddress)
                .where(CustomerAddress.shop_id == x_shop_id)
                .where(CustomerAddress.livemode == livemode)
                .where(CustomerAddress.customer_id == customer_id)
                .where(CustomerAddress.id == address_id)
            )
            address = results.one()
            py_addresses = pydantify_addresses([address])
            return py_addresses.pop()
        except Exception as e:
            print("EXCEPTION retrieve_customer:", e)
            return None


def list_addresses(
    x_shop_id: str,
    livemode: bool,
    customer_id: str,
    skip: str = None,
    limit: int = 50,
) -> list[schema.CustomerAddress]:
    with Session(engine) as db:
        # TODO skip and limit
        results = db.exec(
            select(CustomerAddress)
            .where(CustomerAddress.shop_id == x_shop_id)
            .where(CustomerAddress.livemode == livemode)
            .where(CustomerAddress.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
        )
        all_rows = list(results.all())
        return pydantify_addresses(all_rows)


def delete_address(
    x_shop_id: str,
    livemode: bool,
    customer_id: str,
    address_id: str,
) -> str | None:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(CustomerAddress)
                .where(CustomerAddress.shop_id == x_shop_id)
                .where(CustomerAddress.livemode == livemode)
                .where(CustomerAddress.customer_id == customer_id)
                .where(CustomerAddress.id == address_id)
            )
            address = results.one()
            db.delete(address)
            db.commit()
            return address.id
        except Exception as e:
            print("EXCEPTION delete_address:", e)
            return None
