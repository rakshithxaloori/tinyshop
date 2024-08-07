from sqlmodel import Session, select, update

from variant.model import Variant
from variant import schema
from variant.utils import pydantify_variants
from lib.session import update_instance
from price import crud as price_crud


def create_variant(
    shop_id: str,
    livemode: bool,
    variant: schema.VariantCreate,
    db: Session,
) -> schema.Variant | None:
    try:
        variant_data = variant.model_dump(
            exclude={"product", "package_dimensions", "options"}
        )
        # Create a variant
        new_variant = Variant(
            shop_id=shop_id,
            livemode=livemode,
            product_id=variant.product,
            options="".join(variant.options) if variant.options else None,
            **variant_data,
            **variant.package_dimensions.model_dump(exclude_none=True),
        )
        db.add(new_variant)
        if variant.is_default:
            # Make all other variants is_default False
            db.exec(
                update(Variant)
                .where(Variant.shop_id == shop_id)
                .where(Variant.livemode == livemode)
                .where(Variant.product_id == variant.product)
                .where(Variant.id != new_variant.id)
                .values(is_default=False)
            )

        db.commit()
        db.refresh(new_variant)

        py_variants = pydantify_variants([new_variant])
        return py_variants.pop()
    except Exception as e:
        print("EXCEPTION create_variant:", e)
        return None


def update_variant(
    shop_id: str,
    livemode: bool,
    variant_id: str,
    variant: schema.VariantUpdate,
    db: Session,
) -> schema.Variant | None:
    try:
        variant_data = variant.model_dump(
            exclude={"package_dimensions"}, exclude_none=True
        )

        statement = (
            select(Variant)
            .where(Variant.shop_id == shop_id)
            .where(Variant.livemode == livemode)
            .where(Variant.id == variant_id)
        )
        result = db.exec(statement)
        var_ins = result.one()

        update_instance(db, variant_data, var_ins)
        if variant.is_default:
            # Make all other variants is_default False
            db.exec(
                update(Variant)
                .where(Variant.shop_id == shop_id)
                .where(Variant.livemode == livemode)
                .where(Variant.product_id == var_ins.product_id)
                .where(Variant.id != var_ins.id)
                .values(is_default=False)
            )

        if variant.package_dimensions:
            pd_data = variant.package_dimensions.model_dump(exclude_none=True)
            update_instance(db, pd_data, var_ins)

        db.commit()
        db.refresh(var_ins)
        py_variants = pydantify_variants([var_ins])
        return py_variants.pop()
    except Exception as e:
        print("EXCEPTION update_variant:", e)
        return None


def retrieve_variant(
    shop_id: str,
    livemode: bool,
    variant_id: str,
    db: Session,
) -> schema.Variant | None:
    try:
        results = db.exec(
            select(Variant)
            .where(Variant.shop_id == shop_id)
            .where(Variant.livemode == livemode)
            .where(Variant.id == variant_id)
        )
        row = results.one()
        py_variants = pydantify_variants([row])
        variant = py_variants.pop()
        variant.prices = price_crud.list_prices(
            shop_id,
            livemode,
            variant.id,
            db,
        )
        return variant

    except Exception as e:
        print("EXCEPTION retrieve_variant:", e)
        return None


def list_variants(
    shop_id: str,
    livemode: bool,
    product_id: str,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.VariantList:
    results = db.exec(
        select(Variant)
        .where(Variant.shop_id == shop_id)
        .where(Variant.livemode == livemode)
        .where(Variant.product_id == product_id)
        .offset(skip)
        .limit(limit)
    )
    all_rows = list(results.all())
    variants = pydantify_variants(all_rows)
    for variant in variants:
        # TODO make this db calls efficient
        variant.prices = price_crud.list_prices(
            shop_id,
            livemode,
            variant.id,
            db,
        )
    return schema.VariantList(
        url="/v1/variants",
        has_more=False,  # TODO
        data=variants,
    )


def delete_variant(
    shop_id: str,
    livemode: bool,
    variant_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Variant)
            .where(Variant.shop_id == shop_id)
            .where(Variant.livemode == livemode)
            .where(Variant.id == variant_id)
        )
        variant = results.one()
        db.delete(variant)
        db.commit()
        return variant.id
    except Exception as e:
        print("EXCEPTION delete_variant:", e)
        return None
