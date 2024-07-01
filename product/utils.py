from product.model import Product
from product import schema


def pydantify_products(rows: list[Product]) -> list[schema.Product]:
    products: list[schema.Product] = []
    for product in rows:
        products.append(
            schema.Product(
                **product.model_dump(exclude={"created", "updated"}),
                created=int(product.created.timestamp()),
                updated=int(product.updated.timestamp()),
                # TODO variants, options
            ),
        )
    return products
