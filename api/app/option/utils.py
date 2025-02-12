from app.option.model import Option
from app.option import schema


def pydantify_options(rows: list[Option]) -> list[schema.Option]:
    options: list[schema.Option] = []
    for option in rows:
        options.append(
            schema.Option(
                **option.model_dump(),
            )
        )

    return options
