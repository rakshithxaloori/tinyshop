from product.variant.model import Variant, PackageDimensions
from product.variant import schema


def pydantify_variants(
    rows: list[tuple[Variant, PackageDimensions | None]]
) -> list[schema.Variant]:
    variants: list[schema.Variant] = []
    for variant, pd in rows:
        variants.append(
            schema.Variant(
                **variant.model_dump(exclude={"created", "updated"}),
                created=int(variant.created.timestamp()),
                updated=int(variant.updated.timestamp()),
                package_dimensions=schema.PackageDimensions(**pd.model_dump())
            )
        )
    return variants
