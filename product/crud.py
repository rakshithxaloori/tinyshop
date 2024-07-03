from sqlmodel import Session, select

from product.model import Product
from product import schema
from product.utils import pydantify_products
from lib.session import update_refresh


def create_product(
    shop_id: str,
    livemode: bool,
    product: schema.ProductCreate,
    db: Session,
) -> schema.Product | None:
    try:
        product_data = product.model_dump()
        new_product = Product(
            shop_id=shop_id,
            livemode=livemode,
            **product_data,
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        py_products = pydantify_products([new_product])
        print("PY PRODUCTS", py_products)
        return py_products.pop()
    except Exception as e:
        print("EXCEPTION create_products:", e)
        return None


def update_product(
    shop_id: str,
    livemode: bool,
    product_id: str,
    product: schema.ProductUpdate,
    db: Session,
) -> schema.Product | None:
    try:
        update_data = product.model_dump(exclude_none=True)

        statement = (
            select(Product)
            .where(Product.shop_id == shop_id)
            .where(Product.livemode == livemode)
            .where(Product.id == product_id)
        )
        result = db.exec(statement)
        updated_product = result.one()

        update_refresh(db, update_data, updated_product)
        py_products = pydantify_products([updated_product])
        return py_products.pop()

    except Exception as e:
        print("EXCEPTION update_product:", e)
        return None


def retrieve_product(
    shop_id: str,
    livemode: bool,
    product_id: str,
    db: Session,
) -> schema.Product:
    try:
        results = db.exec(
            select(Product)
            .where(Product.shop_id == shop_id)
            .where(Product.livemode == livemode)
            .where(Product.id == product_id)
        )
        product = results.one()
        py_products = pydantify_products([product])
        return py_products.pop()
    except Exception as e:
        print("EXCEPTION retrieve_product:", e)
        return None


def list_products(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.ProductList:
    subquery = select(Product.id).offset(skip).limit(limit).subquery()

    results = db.exec(
        select(Product)
        .where(Product.shop_id == shop_id)
        .where(Product.livemode == livemode)
        .where(Product.id.in_(subquery))
    )
    all_rows = list(results.all())
    print("ALL ROWS")
    products = pydantify_products(all_rows)
    return schema.ProductList(
        has_more=False,  # TODO
        data=products,
    )


def delete_product(
    shop_id: str,
    livemode: bool,
    product_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Product)
            .where(Product.shop_id == shop_id)
            .where(Product.livemode == livemode)
            .where(Product.id == product_id)
        )
        product = results.one()
        db.delete(product)
        db.commit()
        return product.id
    except Exception as e:
        print("EXCEPTION delete_product:", e)
        return None
