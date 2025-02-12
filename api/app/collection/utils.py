from sqlmodel import Session, select

from app.collection.model import Collection
from app.collection import schema
from app.product import schema as prod_schema
from app.product import utils as prod_utils
from app.lib.limit import LIST_LIMIT_COUNT


def pydantify_collections(rows: list[Collection]) -> list[schema.Collection]:
    collections: list[schema.Collection] = []
    for col_ins in rows:
        collections.append(
            schema.Collection(
                **col_ins.model_dump(exclude={"product_links"}),
                products=schema.ProductList(
                    url=f"/v1/products?collection={col_ins.id}",
                    data=[
                        cp_link.product_id
                        for cp_link in col_ins.product_links[:LIST_LIMIT_COUNT]
                    ],
                    has_more=False,  # TODO
                ),
            )
        )

    return collections


def expand_collection(
    db: Session,
    shop_id: str,
    livemode: bool,
    collection: schema.Collection,
    expand: list[str],
) -> schema.Collection:
    # TODO
    if "products" in expand:
        results = db.exec(
            select(Collection)
            .where(Collection.shop_id == shop_id)
            .where(Collection.livemode == livemode)
            .where(Collection.id == collection.id)
        )
        col_ins = results.one()
        collection.products.data = [
            prod_schema.Product(
                **cp_link.product.model_dump(),
            )
            for cp_link in col_ins.product_links[:LIST_LIMIT_COUNT]
        ]
        collection.products.data = prod_utils.expand_products(
            db,
            shop_id,
            livemode,
            collection.products.data,
            ["default_variant"],
        )
    return collection
