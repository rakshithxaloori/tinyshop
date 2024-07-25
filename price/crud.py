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
        data = price.model_dump(exclude_none=True)

        statement = (
            select(Price)
            .where(Price.shop_id == shop_id)
            .where(Price.livemode == livemode)
            .where(Price.id == price_id)
        )
        result = db.exec(statement)
        price_ins = result.one()
        update_instance(db, data, price_ins)

        cua_ins = None
        if price.customer_unit_amount:
            data = price.customer_unit_amount.model_dump(exclude_none=True)
            statement = select(CustomerUnitAmount).where(
                CustomerUnitAmount.price_id == price_id
            )
            result = db.exec(statement)
            cua_ins = result.one()
            update_instance(db, data, cua_ins)

        recurr_ins = None
        if price.recurring:
            data = price.recurring.model_dump(exclude_none=True)
            statement = select(Recurring).where(Recurring.price_id == price_id)
            result = db.exec(statement)
            recurr_ins = result.one()
            update_instance(db, data, recurr_ins)

        db.commit()
        db.refresh(price_ins)
        if cua_ins:
            db.refresh(cua_ins)
        if recurr_ins:
            db.refresh(recurr_ins)

        py_prices = pydantify_prices([(price_ins, cua_ins, recurr_ins)])
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
    results = db.exec(
        select(Price, CustomerUnitAmount, Recurring)
        .where(Price.shop_id == shop_id)
        .where(Price.livemode == livemode)
        .where(Price.variant_id == variant_id)
        .offset(skip)
        .limit(limit)
        .outerjoin(CustomerUnitAmount, Price.customer_unit_amount)
        .outerjoin(Recurring, Price.recurring)
    )
    all_rows = list(results.all())
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
