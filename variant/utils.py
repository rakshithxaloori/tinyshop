from variant.model import Variant
from variant import schema


def pydantify_variants(rows: list[Variant]) -> list[schema.Variant]:
    variants: list[schema.Variant] = []
    for variant in rows:
        variant_data = variant.model_dump()
        variants.append(
            schema.Variant(
                **variant_data,
                package_dimensions=schema.PackageDimensions(
                    **variant.model_dump(
                        include={"height", "width", "length", "weight"}
                    )
                ),
            )
        )
    return variants
