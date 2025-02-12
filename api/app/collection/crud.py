from sqlmodel import Session, select

from app.collection.model import Collection
from app.collection import schema
from app.product.model import Product
from app.lib.many_to_many_tables import CollectionProductLink
from app.collection.utils import pydantify_collections, expand_collection
from app.lib.session import update_instance
from app.lib.search import Operators
from app.lib.form.handle import get_handle


def create_collection(
    shop_id: str,
    livemode: bool,
    collection: schema.CollectionCreate,
    db: Session,
) -> schema.Collection:
    try:
        col_data = collection.model_dump(exclude={"products"})
        new_col = Collection(
            shop_id=shop_id,
            livemode=livemode,
            handle=get_handle(collection.name),
            **col_data,
        )

        if collection.products:
            prod_res = db.exec(
                select(Product.id)
                .where(Product.shop_id == shop_id)
                .where(Product.livemode == livemode)
                .where(Product.id.in_(collection.products))
            )
            prod_ids = list(prod_res.all())
            for prod_id in prod_ids:
                new_cp_link = CollectionProductLink(
                    livemode=livemode,
                    collection_id=new_col.id,
                    product_id=prod_id,
                )
                new_col.product_links.append(new_cp_link)
                db.add(new_cp_link)
        db.add(new_col)
        db.commit()
        db.refresh(new_col)

        py_collections = pydantify_collections([new_col])
        return py_collections.pop()

    except Exception as e:
        print("EXCEPTION create_collection:", e)
        return None


def update_collection(
    shop_id: str,
    livemode: bool,
    collection_id: str,
    collection: schema.CollectionUpdate,
    db: Session,
) -> schema.Collection:
    try:
        data = collection.model_dump(exclude_none=True, exclude={"products"})
        if collection.name:
            data["handle"] = get_handle(collection.name)
        col_res = db.exec(
            select(Collection)
            .where(Collection.shop_id == shop_id)
            .where(Collection.livemode == livemode)
            .where(Collection.id == collection_id)
        )
        col_ins = col_res.one()

        update_instance(db, data, col_ins)

        products = collection.products
        if products:
            if products.add:
                prod_res = db.exec(
                    select(Product.id)
                    .where(Product.shop_id == shop_id)
                    .where(Product.livemode == livemode)
                    .where(Product.id.in_(products.add))
                )
                prod_ids = list(prod_res.all())
                for prod_id in prod_ids:
                    new_cp_link = CollectionProductLink(
                        livemode=livemode,
                        collection_id=col_ins.id,
                        product_id=prod_id,
                    )
                    col_ins.product_links.append(new_cp_link)
                    db.add(new_cp_link)
            if products.remove:
                cp_links_res = db.exec(
                    select(CollectionProductLink)
                    .where(CollectionProductLink.livemode == livemode)
                    .where(CollectionProductLink.collection_id == col_ins.id)
                    .where(CollectionProductLink.product_id.in_(products.remove))
                )
                cp_links = cp_links_res.all()
                for cp_link in cp_links:
                    db.delete(cp_link)
            db.add(col_ins)
        db.commit()
        db.refresh(col_ins)
        py_collections = pydantify_collections([col_ins])
        return py_collections.pop()

    except Exception as e:
        print("EXCEPTION update_collection:", e)
        return None


def retrieve_collection(
    shop_id: str,
    livemode: bool,
    collection_id: str,
    db: Session,
    expand: list[str] | None = None,
) -> schema.Collection:
    # TODO expand
    try:
        result = db.exec(
            select(Collection)
            .where(Collection.shop_id == shop_id)
            .where(Collection.livemode == livemode)
            .where(Collection.id == collection_id)
        )
        collection = result.one()
        py_collections = pydantify_collections([collection])
        return py_collections.pop()
    except Exception as e:
        print("EXCEPTION retrieve_collection:", e)
        return None


def list_collections(
    shop_id: str,
    livemode: bool,
    db: Session,
    product_id: str | None = None,
    skip: str = None,
    limit: int = 50,
) -> schema.CollectionList:
    # TODO expand
    all_rows = None
    url = "/v1/collections"
    if product_id:
        link_res = db.exec(
            select(CollectionProductLink)
            .where(CollectionProductLink.product_id == product_id)
            .offset(skip)
            .limit(limit)
        )
        all_links = link_res.all()
        all_rows = [link.collection for link in all_links]
        url += f"?product={product_id}"
    else:
        results = db.exec(
            select(Collection)
            .where(Collection.shop_id == shop_id)
            .where(Collection.livemode == livemode)
            .offset(skip)
            .limit(limit)
        )
        all_rows = results.all()
    collections = pydantify_collections(all_rows)
    return schema.CollectionList(
        has_more=False,
        data=collections,
        url=url,
    )


def delete_collection(
    shop_id: str,
    livemode: bool,
    collection_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Collection)
            .where(Collection.shop_id == shop_id)
            .where(Collection.livemode == livemode)
            .where(Collection.id == collection_id)
        )
        collection = results.one()
        db.delete(collection)
        db.commit()
        return collection.id
    except Exception as e:
        print("EXCEPTION delete_collection:", e)
        return None


def search_collections(
    shop_id: str,
    livemode: bool,
    query: str,
    db: Session,
    expand: list[str] | None = None,
) -> schema.CollectionList:
    try:
        clauses = query.split(" ")
        for clause in clauses:
            field, value = clause.split(Operators.SEMI_COLON)
            if field == "handle":
                results = db.exec(
                    select(Collection)
                    .where(Collection.shop_id == shop_id)
                    .where(Collection.livemode == livemode)
                    .where(Collection.handle == value)
                )
                collection_ins = results.one()
                collection = pydantify_collections([collection_ins]).pop()

                if expand:
                    collection = expand_collection(
                        db,
                        shop_id,
                        livemode,
                        collection,
                        expand,
                    )
                return schema.CollectionList(
                    url="/v1/collections/search",
                    has_more=False,  # TODO
                    data=[collection],
                )

        return schema.CollectionList(
            url="/v1/collections/search",
            has_more=False,  # TODO
            data=[],
        )

    except Exception as e:
        print("EXCEPTION search_collections:", e)
        return schema.CollectionList(
            url="/v1/collections/search",
            has_more=False,  # TODO
            data=[],
        )
