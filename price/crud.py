from sqlmodel import Session, select

from price.model import Price, CustomerUnitAmount, Recurring
from price import schema
from price.utils import pydantify_prices
from lib.session import update_instance


def create_price(
    shop_id: str,
    livemode: bool,
    price: schema.PriceCreate,
    db: Session,
) -> schema.Price | None:
    try:
        price_data = price.model_dump(
            exclude={"variant", "customer_unit_amount", "recurring"}
        )

        new_price = Price(
            shop_id=shop_id,
            livemode=livemode,
            variant_id=price.variant,
            **price_data,
        )
        db.add(new_price)

        new_cua = None
        if price.customer_unit_amount:
            cua_data = price.customer_unit_amount.model_dump(exclude_none=True)
            new_cua = CustomerUnitAmount(
                shop_id=shop_id,
                livemode=livemode,
                price_id=new_price.id,
                **cua_data,
            )
            db.add(new_cua)
        new_recurring = None
        if price.recurring:
            recurring_data = price.recurring.model_dump()
            new_recurring = Recurring(
                shop_id=shop_id,
                livemode=livemode,
                price_id=new_price.id,
                **recurring_data,
            )
            db.add(new_recurring)

        db.commit()
        db.refresh(new_price)
        if new_cua:
            db.refresh(new_cua)
        if new_recurring:
            db.refresh(new_recurring)
        print("BEFORE PY", new_price, new_cua, new_recurring)
        py_prices = pydantify_prices([(new_price, new_cua, new_recurring)])
        return py_prices.pop()

    except Exception as e:
        print("EXCEPTION create_price:", e)
        return None


def update_price(
    shop_id: str,
    livemode: bool,
    price_id: str,
    price: schema.PriceCreate,
    db: Session,
) -> schema.Price | None:
    try:
        update_data = price.model_dump(exclude_none=True)

        statement = (
            select(Price)
            .where(Price.shop_id == shop_id)
            .where(Price.livemode == livemode)
            .where(Price.id == price_id)
        )
        result = db.exec(statement)
        updated_price = result.one()
        update_instance(db, update_data, updated_price)

        updated_cua = None
        if price.customer_unit_amount:
            update_data = price.customer_unit_amount.model_dump(exclude_none=True)
            statement = select(CustomerUnitAmount).where(
                CustomerUnitAmount.price_id == price_id
            )
            result = db.exec(statement)
            updated_cua = result.one()
            update_instance(db, update_data, updated_cua)

        updated_recurring = None
        if price.recurring:
            update_data = price.recurring.model_dump(exclude_none=True)
            statement = select(Recurring).where(Recurring.price_id == price_id)
            result = db.exec(statement)
            updated_recurring = result.one()
            update_instance(db, update_data, updated_recurring)

        db.commit()
        db.refresh(updated_price)
        if updated_cua:
            db.refresh(updated_cua)
        if updated_recurring:
            db.refresh(updated_recurring)

        py_prices = pydantify_prices([(updated_price, updated_cua, updated_recurring)])
        return py_prices.pop()
    except Exception as e:
        print("EXCEPTION update_price:", e)
        return None


def retrieve_price(
    shop_id: str,
    livemode: bool,
    price_id: str,
    db: Session,
) -> schema.Price | None:
    try:
        results = db.exec(
            select(Price, CustomerUnitAmount, Recurring)
            .where(Price.shop_id == shop_id)
            .where(Price.livemode == livemode)
            .where(Price.id == price_id)
            .outerjoin(CustomerUnitAmount, Price.customer_unit_amount)
            .outerjoin(Recurring, Price.recurring)
        )
        all_rows = list(results.all())
        py_prices = pydantify_prices(all_rows)
        return py_prices.pop()

    except Exception as e:
        print("EXCEPTION retrieve_price:", e)
        return None


def list_prices(
    shop_id: str,
    livemode: bool,
    variant_id: str,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.PriceList:
    subquery = select(Price.id).offset(skip).limit(limit).subquery()

    results = db.exec(
        select(Price, CustomerUnitAmount, Recurring)
        .where(Price.shop_id == shop_id)
        .where(Price.livemode == livemode)
        .where(Price.variant_id == variant_id)
        .where(Price.id.in_(subquery))
        .outerjoin(CustomerUnitAmount, Price.customer_unit_amount)
        .outerjoin(Recurring, Price.recurring)
    )
    all_rows = list(results.all())
    print("ALL ROWS", all_rows)
    prices = pydantify_prices(all_rows)
    return schema.PriceList(
        has_more=False,  # TODO
        data=prices,
    )


def delete_price(
    shop_id: str,
    livemode: bool,
    price_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Price)
            .where(Price.shop_id == shop_id)
            .where(Price.livemode == livemode)
            .where(Price.id == price_id)
        )
        price = results.one()
        db.delete(price)
        db.commit()
        return price.id
    except Exception as e:
        print("EXCEPTION delete_customer:", e)
        return None
