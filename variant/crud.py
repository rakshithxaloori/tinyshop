from sqlmodel import Session, select

from variant.model import Variant, PackageDimensions
from variant import schema
from variant.utils import pydantify_variants
from lib.session import update_instance


def create_variant(
    shop_id: str,
    livemode: bool,
    variant: schema.VariantCreate,
    db: Session,
) -> schema.Variant | None:
    try:
        variant_data = variant.model_dump(exclude={"product", "package_dimensions"})
        # TODO make this a transaction
        # Create a variant
        new_variant = Variant(
            shop_id=shop_id,
            livemode=livemode,
            product_id=variant.product,
            **variant_data,
        )
        db.add(new_variant)
        db.commit()
        db.refresh(new_variant)

        new_package_dimensions = None
        if variant.package_dimensions:
            pd_data = variant.package_dimensions.model_dump(exclude_none=True)
            new_package_dimensions = PackageDimensions(
                livemode=livemode,
                variant_id=new_variant.id,
                **pd_data,
            )
            db.add(new_package_dimensions)
            db.commit()
            db.refresh(new_variant)
            db.refresh(new_package_dimensions)
        py_variants = pydantify_variants([(new_variant, new_package_dimensions)])
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
        updated_variant = result.one()

        update_instance(db, variant_data, updated_variant)

        pd = None
        if variant.package_dimensions:
            package_dimensions_data = variant.package_dimensions.model_dump(
                exclude_none=True
            )
            statement = select(PackageDimensions).where(
                PackageDimensions.variant_id == variant_id
            )
            # TODO create a pd if it doesn't exist - use merge?
            results = db.exec(statement)
            pd = results.one()

            update_instance(db, package_dimensions_data, pd)
            db.refresh(updated_variant)
        py_variants = pydantify_variants([(updated_variant, pd)])
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
            select(Variant, PackageDimensions)
            .where(Variant.shop_id == shop_id)
            .where(Variant.livemode == livemode)
            .where(Variant.id == variant_id)
            .where(Variant.id == PackageDimensions.variant_id)
        )
        row = results.one()
        py_variants = pydantify_variants([row])
        return py_variants.pop()

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
    subquery = select(Variant.id).offset(skip).limit(limit).subquery()

    results = db.exec(
        select(Variant, PackageDimensions)
        .where(Variant.shop_id == shop_id)
        .where(Variant.livemode == livemode)
        .where(Variant.product_id == product_id)
        .where(Variant.id.in_(subquery))
        .where(Variant.id == PackageDimensions.variant_id)
    )
    all_rows = list(results.all())
    variants = pydantify_variants(all_rows)
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
