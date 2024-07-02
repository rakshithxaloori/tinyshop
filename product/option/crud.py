from sqlmodel import Session, select

from product.model import Product
from product.option.model import Option
from product.option import schema
from product.option.utils import pydantify_options
from database import engine


def create_option(
    x_shop_id: str,
    livemode: bool,
    option: schema.OptionCreate,
) -> schema.Option | None:
    with Session(engine) as db:
        try:
            prod_results = db.exec(
                select(Product)
                .where(Product.shop_id == x_shop_id)
                .where(Product.livemode == livemode)
                .where(Product.id == option.product)
            )
            product = prod_results.one()
            option_data = option.model_dump()
            new_option = Option(
                shop_id=x_shop_id,
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
    x_shop_id: str,
    livemode: bool,
    option_id: str,
    option: schema.OptionUpdate,
) -> schema.Option | None:
    with Session(engine) as db:
        try:
            update_data = option.model_dump(exclude_none=True)

            statement = (
                select(Option)
                .where(Option.shop_id == x_shop_id)
                .where(Option.livemode == livemode)
                .where(Option.id == option_id)
            )
            result = db.exec(statement)
            updated_option = result.one()

            for key, value in update_data.items():
                setattr(updated_option, key, value)

            db.add(updated_option)
            db.commit()
            db.refresh(updated_option)
            py_options = pydantify_options([updated_option])
            return py_options.pop()
        except Exception as e:
            print("EXCEPTION update_option:", e)
            return None


def retrieve_option(
    x_shop_id: str,
    livemode: bool,
    option_id: str,
) -> schema.Option | None:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(Option)
                .where(Option.shop_id == x_shop_id)
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
    x_shop_id: str,
    livemode: bool,
    skip: str = None,
    limit: int = 50,
) -> schema.OptionList:
    with Session(engine) as db:
        results = db.exec(
            select(Option)
            .where(Option.shop_id == x_shop_id)
            .where(Option.livemode == livemode)
        )
        all_rows = list(results.all())
        options = pydantify_options(all_rows)
        schema.OptionList(
            url="/v1/options",
            has_more=False,  # TODO
            data=options,
        )


def delete_option(
    x_shop_id: str,
    livemode: bool,
    option_id: str,
) -> schema.OptionDelete:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(Option)
                .where(Option.shop_id == x_shop_id)
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
