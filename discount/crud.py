from sqlmodel import Session, select

from discount.model import Discount
from discount import schema
from customer.model import Customer
from discount.utils import pydantify_discounts
from lib.session import update_instance


def create_discount(
    shop_id: str,
    livemode: bool,
    discount: schema.DiscountCreate,
    db: Session,
) -> schema.Discount | None:
    try:
        discount_data = discount.model_dump(exclude={"customers"})
        customers_select = []
        if discount.customers:
            cus_results = db.exec(
                select(Customer)
                .where(Customer.shop_id == shop_id)
                .where(Customer.livemode == livemode)
                .where(Customer.id.in_(discount.customers))
            )
            customers_select = list(cus_results.all())

        new_discount = Discount(
            shop_id=shop_id,
            livemode=livemode,
            customers_select=customers_select,
            **discount_data,
        )
        db.add(new_discount)
        db.commit()
        db.refresh(new_discount)

        py_discounts = pydantify_discounts([new_discount])
        return py_discounts.pop()

    except Exception as e:
        print("EXCEPTION create_discount:", e)
        return None


def update_discount(
    shop_id: str,
    livemode: bool,
    discount_id: str,
    discount: schema.DiscountUpdate,
    db: Session,
) -> schema.Discount | None:
    try:
        data = discount.model_dump(exclude_none=True, exclude={"customers"})
        statement = (
            select(Discount)
            .where(Discount.shop_id == shop_id)
            .where(Discount.livemode == livemode)
            .where(Discount.id == discount_id)
        )
        results = db.exec(statement)
        discount_ins = results.one()
        customers = discount.customers
        if customers:
            if customers.add:
                # Add these customers
                add_res = db.exec(
                    select(Customer)
                    .where(Customer.shop_id == shop_id)
                    .where(Customer.livemode == livemode)
                    .where(Customer.id.in_(customers.add))
                )
                all_cus_add = list(add_res.all())
                discount_ins.customers_select.extend(all_cus_add)
            if customers.remove:
                # Remove these customers
                rm_res = db.exec(
                    select(Customer)
                    .where(Customer.shop_id == shop_id)
                    .where(Customer.livemode == livemode)
                    .where(Customer.id.in_(customers.remove))
                )
                all_cus_rm = list(rm_res.all())
                for cus_rm in all_cus_rm:
                    discount_ins.customers_select.remove(cus_rm)

        update_instance(db, data, discount_ins)
        db.commit()
        db.refresh(discount_ins)
        py_discounts = pydantify_discounts([discount_ins])
        return py_discounts.pop()

    except Exception as e:
        print("EXCEPTION update_discount:", e)
        return None


def retrieve_discount(
    shop_id: str,
    livemode: bool,
    discount_id: str,
    db: Session,
) -> schema.Discount | None:
    try:
        results = db.exec(
            select(Discount)
            .where(Discount.shop_id == shop_id)
            .where(Discount.livemode == livemode)
            .where(Discount.id == discount_id)
        )
        discount = results.one()
        py_discounts = pydantify_discounts([discount])
        return py_discounts.pop()
    except Exception as e:
        print("EXCEPTION retrieve_discount:", e)
        return None


def list_discounts(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.DiscountList:
    subquery = select(Discount.id).offset(skip).limit(limit).subquery()

    results = db.exec(
        select(Discount)
        .where(Discount.shop_id == shop_id)
        .where(Discount.livemode == livemode)
        .where(Discount.id.in_(subquery))
    )
    all_rows = list(results.all())
    discounts = pydantify_discounts(all_rows)
    return schema.DiscountList(
        has_more=False,
        data=discounts,
    )


def delete_discount(
    shop_id: str,
    livemode: bool,
    discount_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Discount)
            .where(Discount.shop_id == shop_id)
            .where(Discount.livemode == livemode)
            .where(Discount.id == discount_id)
        )
        discount = results.one()
        db.delete(discount)
        db.commit()
        return discount.id
    except Exception as e:
        print("EXCEPTION delete_discount:", e)
        return None
