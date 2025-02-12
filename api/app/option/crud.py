from sqlmodel import Session, select

from app.product.model import Product
from app.option.model import Option
from app.option import schema
from app.option.utils import pydantify_options
from app.lib.session import update_instance


def create_option(
    shop_id: str,
    livemode: bool,
    option: schema.OptionCreate,
    db: Session,
) -> schema.Option | None:
    try:
        prod_results = db.exec(
            select(Product)
            .where(Product.shop_id == shop_id)
            .where(Product.livemode == livemode)
            .where(Product.id == option.product)
        )
        product = prod_results.one()
        option_data = option.model_dump(exclude={"product"})
        new_option = Option(
            shop_id=shop_id,
            livemode=livemode,
            product_id=product.id,
            **option_data,
        )
        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        py_options = pydantify_options([new_option])
        return py_options.pop()
    except Exception as e:
        print("EXCEPTION create_option", e)
        return None


def update_option(
    shop_id: str,
    livemode: bool,
    option_id: str,
    option: schema.OptionUpdate,
    db: Session,
) -> schema.Option | None:
    try:
        data = option.model_dump(exclude_none=True)

        statement = (
            select(Option)
            .where(Option.shop_id == shop_id)
            .where(Option.livemode == livemode)
            .where(Option.id == option_id)
        )
        result = db.exec(statement)
        option_ins = result.one()

        update_instance(db, data, option_ins)
        db.commit()
        db.refresh(option_ins)
        py_options = pydantify_options([option_ins])
        return py_options.pop()
    except Exception as e:
        print("EXCEPTION update_option:", e)
        return None


def retrieve_option(
    shop_id: str,
    livemode: bool,
    option_id: str,
    db: Session,
) -> schema.Option | None:
    try:
        results = db.exec(
            select(Option)
            .where(Option.shop_id == shop_id)
            .where(Option.livemode == livemode)
            .where(Option.id == option_id)
        )
        option = results.one()
        py_options = pydantify_options([option])
        return py_options.pop()
    except Exception as e:
        print("EXCEPTION retrieve_option:", e)
        return None


def list_options(
    shop_id: str,
    livemode: bool,
    product_id: str,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.OptionList:
    results = db.exec(
        select(Option)
        .where(Option.shop_id == shop_id)
        .where(Option.livemode == livemode)
        .where(Option.product_id == product_id)
        .offset(skip)
        .limit(limit)
    )
    all_rows = list(results.all())
    options = pydantify_options(all_rows)
    return schema.OptionList(
        url="/v1/options",
        has_more=False,  # TODO
        data=options,
    )


def delete_option(
    shop_id: str,
    livemode: bool,
    option_id: str,
    db: Session,
) -> schema.OptionDelete:
    try:
        results = db.exec(
            select(Option)
            .where(Option.shop_id == shop_id)
            .where(Option.livemode == livemode)
            .where(Option.id == option_id)
        )
        option = results.one()
        db.delete(option)
        db.commit()
        return option.id
    except Exception as e:
        print("EXCEPTION delete_option:", e)
        return None
