from collection.model import Collection
from collection import schema


EXPAND_LIMIT = 20


def pydantify_collections(rows: list[Collection]) -> list[schema.Collection]:
    collections: list[schema.Collection] = []
    for col_ins in rows:
        collections.append(
            schema.Collection(
                **col_ins.model_dump(exclude={"created", "updated", "product_links"}),
                created=int(col_ins.created.timestamp()),
                updated=int(col_ins.updated.timestamp()),
                products=schema.ProductList(
                    url=f"/v1/products?collection={col_ins.id}",
                    data=[
                        cp_link.product_id
                        for cp_link in col_ins.product_links[:EXPAND_LIMIT]
                    ],
                    has_more=False,  # TODO
                ),
            )
        )

    return collections
