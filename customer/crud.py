from datetime import datetime, timedelta
from sqlmodel import Session, select

from user.model import User
from customer.model import Customer
from customer import schema
from customer.utils import pydantify_customers, send_otp
from lib.session import update_instance


def create_customer(
    shop_id: str,
    livemode: bool,
    customer: schema.CustomerCreate,
    db: Session,
) -> schema.Customer | None:
    try:
        customer_data = customer.model_dump(exclude={"address"})
        phone = customer.phone
        user: User = None
        try:
            user_res = db.exec(
                select(User).where(livemode == livemode).where(User.phone == phone)
            )
            user = user_res.one()
        except Exception:
            # Create user
            new_user = User(
                livemode=livemode,
                **customer_data,
            )
            db.add(new_user)
            user = new_user

        customer_ins = None
        try:
            cus_res = db.exec(
                select(Customer)
                .where(Customer.shop_id == shop_id)
                .where(Customer.livemode == livemode)
                .where(Customer.user_id == user.id)
            )
            customer_ins = cus_res.one()
            if customer.send_otp:
                new_otp = send_otp(livemode, phone)
                customer_ins.otp = new_otp
                customer_ins.is_verified = False
                customer_ins.expires_at = (
                    int((datetime.now() + timedelta(minutes=10)).timestamp())
                    if customer.send_otp
                    else None
                )
                db.add(customer_ins)

        except Exception:
            # Create a customer
            new_otp = None
            if customer.send_otp:
                new_otp = send_otp(livemode, phone)
            customer_ins = Customer(
                shop_id=shop_id,
                livemode=livemode,
                user_id=user.id,
                otp=new_otp,
                expires_at=(
                    int((datetime.now() + timedelta(minutes=10)).timestamp())
                    if customer.send_otp
                    else None
                ),
            )
            db.add(customer_ins)
        db.commit()
        db.refresh(customer_ins)

        py_customers = pydantify_customers([customer_ins])
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
        data = customer.model_dump(exclude_none=True, exclude={"send_otp", "otp"})

        statement = (
            select(Customer)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == customer_id)
        )
        result = db.exec(statement)
        cus_ins = result.one()

        if customer.otp:
            # Verify the OTP
            if (
                customer.otp == cus_ins.otp
                and int(datetime.now().timestamp()) < cus_ins.expires_at
            ):
                cus_ins.is_verified = True
            else:
                # TODO throw exception
                pass
        elif customer.send_otp and not customer.phone:
            cus_ins.is_verified = False
            new_otp = send_otp(livemode, cus_ins.user.phone)
            cus_ins.otp = new_otp
            cus_ins.expires_at = (
                int((datetime.now() + timedelta(minutes=10)).timestamp())
                if customer.send_otp
                else None
            )
        else:
            update_instance(db, data, cus_ins.user)
            if customer.phone:
                cus_ins.is_verified = False
                new_otp = None
                if customer.send_otp:
                    new_otp = send_otp(livemode, customer.phone)
                cus_ins.otp = new_otp
                cus_ins.expires_at = (
                    int((datetime.now() + timedelta(minutes=10)).timestamp())
                    if customer.send_otp
                    else None
                )

        db.commit()
        db.refresh(cus_ins)
        py_customers = pydantify_customers([cus_ins])
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
            select(Customer)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == customer_id)
        )
        cus = results.one()
        py_customers = pydantify_customers([cus])
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
    results = db.exec(
        select(Customer)
        .where(Customer.shop_id == shop_id)
        .where(Customer.livemode == livemode)
        .offset(skip)
        .limit(limit)
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
