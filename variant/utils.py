from variant.model import Variant, PackageDimensions
from variant import schema


def pydantify_variants(
    rows: list[tuple[Variant, PackageDimensions | None]]
) -> list[schema.Variant]:
    variants: list[schema.Variant] = []
    for variant, pd in rows:
        variant_data = variant.model_dump(
            exclude={"created", "updated", "package_dimensions"}
        )
        if pd:
            pd_data = pd.model_dump()
        variants.append(
            schema.Variant(
                **variant_data,
                created=int(variant.created.timestamp()),
                updated=int(variant.updated.timestamp()),
                package_dimensions=schema.PackageDimensions(**pd_data) if pd else None,
            )
        )
    return variants
