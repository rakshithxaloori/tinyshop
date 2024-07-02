from sqlmodel import Session, select

from product.variant.model import Variant, PackageDimensions
from product.variant import schema
from product.variant.utils import pydantify_variants


def create_variant(
    x_shop_id: str,
    livemode: bool,
    variant: schema.VariantCreate,
    db: Session,
) -> schema.Variant | None:
    with db.begin():
        try:
            variant_data = variant.model_dump(exclude={"package_dimensions"})
            # TODO make this a transaction
            # Create a variant
            new_variant = Variant(
                shop_id=x_shop_id,
                livemode=livemode,
                product_id=Variant.product_id,
                **variant_data,
            )
            db.add(new_variant)
            db.commit()
            db.refresh(new_variant)

            new_package_dimensions = None
            if variant.package_dimensions:
                pd_data = variant.package_dimensions.model_dump(exclude_none=True)
                new_package_dimensions = PackageDimensions(
                    shop_id=x_shop_id,
                    livemode=livemode,
                    variant_id=new_variant.id,
                    **pd_data,
                )
                db.add(new_package_dimensions)
                db.commit()
                db.refresh(new_package_dimensions)
            py_variants = pydantify_variants([(new_variant, new_package_dimensions)])
            return py_variants.pop()
        except Exception as e:
            print("EXCEPTION create_variant:", e)
            return None


def update_variant(
    x_shop_id: str,
    livemode: bool,
    variant_id: str,
    variant: schema.VariantCreate,
    db: Session,
) -> schema.Variant | None:
    with db.begin():
        try:
            variant_data = variant.model_dump(
                exclude={"package_dimensions"}, exclude_none=True
            )

            statement = (
                select(Variant)
                .where(Variant.shop_id == x_shop_id)
                .where(Variant.livemode == livemode)
                .where(Variant.id == variant_id)
            )
            result = db.exec(statement)
            updated_variant = result.one()

            for key, value in variant_data.items():
                setattr(updated_variant, key, value)

            # TODO testing merge here, if works, change it in other places
            db.merge(updated_variant)  # upsert + refresh
            db.commit()
            # db.refresh(updated_variant)
            package_dimensions_data = variant.package_dimensions.model_dump(
                exclude_none=True
            )
            updated_pd = None
            if package_dimensions_data:
                statement = select(PackageDimensions).where(
                    PackageDimensions.variant_id == variant_id
                )
                results = db.exec()
                updated_pd = results.one()

                for key, value in package_dimensions_data.items():
                    setattr(updated_pd, key, value)

                db.merge(updated_pd)
                db.commit()
            py_variants = pydantify_variants([(updated_variant, updated_pd)])
            return py_variants.pop()
        except Exception as e:
            print("EXCEPTION update_variant:", e)
            return None


def retrieve_variant(
    x_shop_id: str,
    livemode: bool,
    id: str,
    db: Session,
) -> schema.Variant | None:
    with db.begin():
        try:
            results = db.exec(
                select(Variant, PackageDimensions)
                .where(Variant.shop_id == x_shop_id)
                .where(Variant.livemode == livemode)
                .where(Variant.id == id)
                .where(Variant.id == PackageDimensions.variant_id)
            )
            row = results.one()
            py_variants = pydantify_variants([row])
            return py_variants.pop()

        except Exception as e:
            print("EXCEPTION retrieve_variant:", e)
            return None


def list_variants(
    x_shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.VariantList:
    with db.begin():
        subquery = select(Variant).offset(skip).limit(limit).subquery()

        results = db.exec(
            select(Variant, PackageDimensions)
            .where(Variant.shop_id == x_shop_id)
            .where(Variant.livemode == livemode)
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
    x_shop_id: str,
    livemode: bool,
    id: str,
    db: Session,
) -> str | None:
    with db.begin():
        try:
            results = db.exec(
                select(Variant)
                .where(Variant.shop_id == x_shop_id)
                .where(Variant.livemode == livemode)
                .where(Variant.id == id)
            )
            variant = results.one()
            db.delete(variant)
            db.commit()
            return variant.id
        except Exception as e:
            print("EXCEPTION delete_variant:", e)
            return None
