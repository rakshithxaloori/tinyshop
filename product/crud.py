from sqlmodel import Session, select

from product.model import Product
from product import schema
from product.utils import pydantify_products
from database import engine


def create_product(
    x_shop_id: str,
    livemode: bool,
    product: schema.ProductCreate,
) -> schema.Product | None:
    with Session(engine) as db:
        try:
            product_data = product.model_dump()
            new_product = Product(
                shop_id=x_shop_id,
                livemode=livemode,
                **product_data,
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            print("AFTER REFRESH")
            py_products = pydantify_products([new_product])
            print("PY PRODUCTS", py_products)
            return py_products.pop()
        except Exception as e:
            print("EXCEPTION create_products:", e)
            return None


def update_product(
    x_shop_id: str,
    livemode: bool,
    product_id: str,
    product: schema.ProductUpdate,
) -> schema.Product | None:
    with Session(engine) as db:
        try:
            update_data = product.model_dump(exclude_none=True)

            statement = (
                select(Product)
                .where(Product.shop_id == x_shop_id)
                .where(Product.livemode == livemode)
                .where(Product.id == product_id)
            )
            result = db.exec(statement)
            updated_product = result.one()

            for key, value in update_data.items():
                setattr(updated_product, key, value)

            db.add(updated_product)
            db.commit()
            db.refresh(updated_product)
            py_products = pydantify_products([updated_product])
            return py_products.pop()

        except Exception as e:
            print("EXCEPTION update_product:", e)
            return None


def retrieve_product(
    x_shop_id: str,
    livemode: bool,
    id: str,
) -> schema.Product:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(Product)
                .where(Product.shop_id == x_shop_id)
                .where(Product.livemode == livemode)
                .where(Product.id == id)
            )
            product = results.one()
            py_products = pydantify_products([product])
            return py_products.pop()
        except Exception as e:
            print("EXCEPTION retrieve_product:", e)
            return None


def list_products(
    x_shop_id: str,
    livemode: bool,
    skip: str = None,
    limit: int = 50,
) -> list[schema.Product]:
    with Session(engine) as db:
        subquery = select(Product.id).offset(skip).limit(limit).subquery()

        results = db.exec(
            select(Product)
            .where(Product.shop_id == x_shop_id)
            .where(Product.livemode == livemode)
            .where(Product.id.in_(subquery))
        )
        all_rows = list(results.all())
        return pydantify_products(all_rows)


def delete_product(
    x_shop_id: str,
    livemode: bool,
    id: str,
) -> str | None:
    with Session(engine) as db:
        try:
            results = db.exec(
                select(Product)
                .where(Product.shop_id == x_shop_id)
                .where(Product.livemode == livemode)
                .where(Product.id == id)
            )
            product = results.one()
            db.delete(product)
            db.commit()
            return product.id
        except Exception as e:
            print("EXCEPTION delete_product:", e)
            return None
