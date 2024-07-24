from sqlmodel import Session, select

from product.model import Product
from product import schema
from product.utils import pydantify_products, expand_product, expand_products
from lib.session import update_instance
from lib.search import Operators
from lib.form.handle import get_handle
from lib.many_to_many_tables import CollectionProductLink


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
            handle=get_handle(product.name),
            **product_data,
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        py_products = pydantify_products([new_product])
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
        data = product.model_dump(exclude_none=True)
        if product.name:
            data["handle"] = get_handle(product.name)

        statement = (
            select(Product)
            .where(Product.shop_id == shop_id)
            .where(Product.livemode == livemode)
            .where(Product.id == product_id)
        )
        result = db.exec(statement)
        prod_ins = result.one()

        update_instance(db, data, prod_ins)
        db.commit()
        db.refresh(prod_ins)
        py_products = pydantify_products([prod_ins])
        return py_products.pop()

    except Exception as e:
        print("EXCEPTION update_product:", e)
        return None


def retrieve_product(
    shop_id: str,
    livemode: bool,
    product_id: str,
    expand: list[str] | None,
    db: Session,
) -> schema.Product:
    try:
        results = db.exec(
            select(Product)
            .where(Product.shop_id == shop_id)
            .where(Product.livemode == livemode)
            .where(Product.id == product_id)
        )

        product_row = results.one()

        py_products = pydantify_products([product_row])
        product = py_products.pop()
        if expand:
            product = expand_product(
                db,
                shop_id,
                livemode,
                product,
                expand,
            )
        return product
    except Exception as e:
        print("EXCEPTION retrieve_product:", e)
        return None


def list_products(
    shop_id: str,
    livemode: bool,
    db: Session,
    expand: list[str] | None = None,
    collection_id: str | None = None,
    skip: str = None,
    limit: int = 50,
) -> schema.ProductList:
    product_rows = None
    url = "/v1/products"
    if collection_id:
        link_res = db.exec(
            select(CollectionProductLink)
            .where(CollectionProductLink.collection_id == collection_id)
            .offset(skip)
            .limit(limit)
        )
        all_links = link_res.all()
        product_rows = [link.product for link in all_links]
        url += f"?collection={collection_id}"
    else:
        results = db.exec(
            select(Product)
            .where(Product.shop_id == shop_id)
            .where(Product.livemode == livemode)
            .offset(skip)
            .limit(limit)
        )
        product_rows = list(results.all())
    products = pydantify_products(product_rows)
    if expand:
        products = expand_products(
            db,
            shop_id,
            livemode,
            products,
            expand,
        )

    return schema.ProductList(
        has_more=False,  # TODO
        data=products,
        url=url,
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


def search_products(
    shop_id: str,
    livemode: bool,
    query: str,
    expand: list[str] | None,
    db: Session,
) -> schema.ProductList:
    try:
        # TODO write a more comprehensive query parser
        clauses = query.split(" ")
        for clause in clauses:
            field, value = clause.split(Operators.SEMI_COLON)
            if field == "handle":
                results = db.exec(
                    select(Product)
                    .where(Product.shop_id == shop_id)
                    .where(Product.livemode == livemode)
                    .where(Product.handle == value)
                )
                product_ins = results.one()
                product = pydantify_products([product_ins]).pop()
                if expand:
                    product = expand_product(
                        db,
                        shop_id,
                        livemode,
                        product,
                        expand,
                    )
                return schema.ProductList(
                    url="/v1/products/search",
                    has_more=False,  # TODO
                    data=[product],
                )

        return schema.ProductList(
            url="/v1/products/search",
            has_more=False,  # TODO
            data=[],
        )

    except Exception as e:
        print("EXCEPTION search_products:", e)
        return schema.ProductList(
            url="/v1/products/search",
            has_more=False,
            data=[],
        )
