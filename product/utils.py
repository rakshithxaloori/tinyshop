from sqlmodel import Session, select

from product.model import Product
from product import schema
from option import crud as opt_crud
from variant.model import Variant
from variant import crud as variant_crud


def pydantify_products(rows: list[Product]) -> list[schema.Product]:
    products: list[schema.Product] = []
    for product in rows:
        products.append(
            schema.Product(
                **product.model_dump(exclude={"created", "updated"}),
                created=int(product.created.timestamp()),
                updated=int(product.updated.timestamp()),
            ),
        )
    return products


def expand_product(
    db: Session,
    shop_id: str,
    livemode: bool,
    product: schema.Product,
    expand: list[str],
) -> schema.Product:
    if "options" in expand:

        product.options = opt_crud.list_options(
            shop_id,
            livemode,
            product.id,
            db,
        )

    if "default_variant" in expand:
        variant_res = db.exec(
            select(Variant.id)
            .where(Variant.shop_id == shop_id)
            .where(Variant.livemode == livemode)
            .where(Variant.product_id == product.id)
            .where(Variant.is_default.is_(True))
            .limit(1)
        )
        variant_id = variant_res.one()
        product.default_variant = variant_crud.retrieve_variant(
            shop_id,
            livemode,
            variant_id,
            db,
        )

    if "variants" in expand:
        product.variants = variant_crud.list_variants(
            shop_id,
            livemode,
            product.id,
            db,
        )

    return product


def expand_products(
    db: Session,
    shop_id: str,
    livemode: bool,
    products: list[schema.Product],
    expand: list[str],
) -> list[schema.Product]:
    products_dict: dict[str, schema.Product] = {p.id: p for p in products}
    if "default_variant" in expand:
        variants_res = db.exec(
            select(Variant.id, Variant.product_id)
            .where(Variant.shop_id == shop_id)
            .where(Variant.livemode == livemode)
            .where(Variant.product_id.in_(products_dict.keys()))
            .where(Variant.is_default.is_(True))
        )
        all_rows = variants_res.all()

        for variant_id, product_id in all_rows:
            products_dict[product_id].default_variant = variant_crud.retrieve_variant(
                shop_id,
                livemode,
                variant_id,
                db,
            )

    return list(products_dict.values())
