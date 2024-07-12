from datetime import datetime
from typing import Annotated
from fastapi import Form


from variant import schema


def create_variant_form(
    product: Annotated[str, Form()],
    name: Annotated[str, Form()],
    active: Annotated[str, Form()],
    accept_zero_inventory_orders: Annotated[str, Form()],
    next_refill: Annotated[str, Form()],  # TODO
    is_default: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
    options: Annotated[list[str] | None, Form()] = None,
    package_dimensions_height: Annotated[
        str | None, Form(alias="package_dimensions[height]")
    ] = None,
    package_dimensions_width: Annotated[
        str | None, Form(alias="package_dimensions[width]")
    ] = None,
    package_dimensions_length: Annotated[
        str | None, Form(alias="package_dimensions[length]")
    ] = None,
    package_dimensions_weight: Annotated[
        str | None, Form(alias="package_dimensions[weight]")
    ] = None,
) -> schema.VariantCreate:
    package_dimensions = None
    if (
        package_dimensions_height
        and package_dimensions_width
        and package_dimensions_length
        and package_dimensions_weight
    ):
        package_dimensions = schema.PackageDimensions(
            height=package_dimensions_height,
            width=package_dimensions_width,
            length=package_dimensions_length,
            weight=package_dimensions_weight,
        )

        schema.PackageDimensions.model_validate(package_dimensions)

    option_values = None
    if options:
        option_values = [
            schema.VariantOptionValue(
                name=o.split(":")[0],
                value=o.split(":")[1],
            )
            for o in options
        ]
    return schema.VariantCreate(
        product=product,
        name=name,
        description=description,
        active=active == "true",
        options=option_values,
        accept_zero_inventory_orders=accept_zero_inventory_orders == "true",
        # TODO convert string to datetime timestamp
        next_refill=datetime.now(),
        package_dimensions=package_dimensions,
        is_default=is_default == "true",
    )


def update_variant_form(
    name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    active: Annotated[str | None, Form()] = None,
    options: Annotated[list[str] | None, Form()] = None,
    accept_zero_inventory_orders: Annotated[str | None, Form()] = None,
    next_refill: Annotated[str | None, Form()] = None,
    is_default: Annotated[str | None, Form()] = None,
    package_dimensions_height: Annotated[
        str | None, Form(alias="package_dimensions[height]")
    ] = None,
    package_dimensions_width: Annotated[
        str | None, Form(alias="package_dimensions[width]")
    ] = None,
    package_dimensions_length: Annotated[
        str | None, Form(alias="package_dimensions[length]")
    ] = None,
    package_dimensions_weight: Annotated[
        str | None, Form(alias="package_dimensions[weight]")
    ] = None,
) -> schema.VariantUpdate:
    package_dimensions = schema.PackageDimensionsUpdate()
    if package_dimensions_height:
        package_dimensions.height = package_dimensions_height
    if package_dimensions_width:
        package_dimensions.width = package_dimensions_width
    if package_dimensions_length:
        package_dimensions.length = package_dimensions_length
    if package_dimensions_weight:
        package_dimensions.weight = package_dimensions_weight
    schema.PackageDimensionsUpdate.model_validate(package_dimensions)

    option_values = None
    if options:
        option_values = [
            schema.VariantOptionValue(
                name=o.split(":")[0],
                value=o.split(":")[1],
            )
            for o in options
        ]
    return schema.VariantUpdate(
        name=name,
        description=description,
        active=active == "true" if active else None,
        options=option_values,
        accept_zero_inventory_orders=accept_zero_inventory_orders == "true",
        # TODO convert string to datetime timestamp
        next_refill=int(datetime.now().timestamp()),
        package_dimensions=package_dimensions,
        is_default=is_default == "true" if is_default else None,
    )
