from product.option.model import Option
from product.option import schema


def pydantify_options(rows: list[Option]) -> list[schema.Option]:
    options: list[schema.Option] = []
    for option in rows:
        options.append(
            schema.Option(
                **option.model_dump(
                    exclude={"created", "updated"},
                    created=int(option.created.timestamp()),
                    updated=int(option.updated.timestamp()),
                )
            )
        )

    return options
