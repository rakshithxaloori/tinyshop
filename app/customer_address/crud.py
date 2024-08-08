from sqlmodel import Session, select

from app.user_address.model import UserAddress
from app.customer.model import Customer
from app.customer_address import schema
from app.customer_address.utils import pydantify_addresses
from app.lib.session import update_instance


def create_address(
    shop_id: str,
    livemode: bool,
    address: schema.CustomerAddressCreate,
    db: Session,
) -> schema.CustomerAddress | None:
    try:
        cus_result = db.exec(
            select(Customer)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == address.customer)
        )
        customer = cus_result.one()
        address_data = address.model_dump(exclude={"customer"})
        # Create the address
        new_user_addresss = UserAddress(
            livemode=livemode,
            user_id=customer.user.id,
            **address_data,
        )
        db.add(new_user_addresss)
        db.commit()
        db.refresh(new_user_addresss)
        py_addresses = pydantify_addresses([new_user_addresss])
        return py_addresses.pop()
    except Exception as e:
        print("EXCEPTION create_address:", e)
        return None


def update_address(
    shop_id: str,
    livemode: bool,
    address_id: str,
    address: schema.CustomerAddressUpdate,
    db: Session,
) -> schema.CustomerAddress | None:
    try:
        # TODO check if the shop has access to this customer
        data = address.model_dump(exclude_none=True)

        statement = (
            select(UserAddress)
            .where(UserAddress.livemode == livemode)
            .where(UserAddress.id == address_id)
        )
        result = db.exec(statement)
        addr_ins = result.one()

        update_instance(db, data, addr_ins)
        db.commit()
        db.refresh(addr_ins)
        py_addresses = pydantify_addresses([addr_ins])
        return py_addresses.pop()
    except Exception as e:
        print("EXCEPTION update_address:", e)
        return None


def retrieve_address(
    shop_id: str,
    livemode: bool,
    address_id: str,
    db: Session,
) -> schema.CustomerAddress | None:
    try:
        # TODO check if the shop has access to this customer
        results = db.exec(
            select(UserAddress)
            .where(UserAddress.livemode == livemode)
            .where(UserAddress.id == address_id)
        )
        address = results.one()
        py_addresses = pydantify_addresses([address])
        return py_addresses.pop()
    except Exception as e:
        print("EXCEPTION retrieve_customer:", e)
        return None


def list_addresses(
    shop_id: str,
    livemode: bool,
    customer_id: str,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.CustomerAddressList:
    # TODO skip and limit
    cus_res = db.exec(
        select(Customer)
        .where(Customer.shop_id == shop_id)
        .where(Customer.livemode == livemode)
        .where(Customer.id == customer_id)
    )
    customer = cus_res.one()
    results = db.exec(
        select(UserAddress)
        .where(UserAddress.livemode == livemode)
        .where(UserAddress.user_id == customer.user_id)
        .offset(skip)
        .limit(limit)
    )
    all_rows = list(results.all())
    addresses = pydantify_addresses(all_rows)
    return schema.CustomerAddressList(
        url="/v1/customers/{customer_id}/addresses".format(customer_id=customer_id),
        has_more=False,
        data=addresses,
    )


def delete_address(
    shop_id: str,
    livemode: bool,
    address_id: str,
    db: Session,
) -> str | None:
    try:
        # TODO check if the shop has access to this customer
        # TODO only delete if no checkouts and subscriptions
        results = db.exec(
            select(UserAddress)
            .where(UserAddress.livemode == livemode)
            .where(UserAddress.id == address_id)
        )
        address = results.one()
        db.delete(address)
        db.commit()
        return address.id
    except Exception as e:
        print("EXCEPTION delete_address:", e)
        return None
