from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Form


from product.variant import schema, crud
from utils.dependencies import ShopIDDep, LivemodeDep
from utils.form import bool_string


router = APIRouter(prefix="/v1/variants")


def create_variant_form(
    name: Annotated[str, Form()],
    active: Annotated[str, Form()],
    accept_zero_inventory_orders: Annotated[str, Form()],
    next_refill: Annotated[str, Form()],
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
):
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

        package_dimensions.model_validate()

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
        name=name,
        description=description,
        active=active == bool_string.TRUE,
        options=option_values,
        accept_zero_inventory_orders=accept_zero_inventory_orders == bool_string.TRUE,
        # TODO convert string to datetime timestamp
        next_refill=int(datetime.now().timestamp()),
        package_dimensions=package_dimensions,
    )


def update_variant_form(
    name: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
    active: Annotated[str | None, Form()] = None,
    options: Annotated[list[str] | None, Form()] = None,
    accept_zero_inventory_orders: Annotated[str | None, Form()] = None,
    next_refill: Annotated[str | None, Form()] = None,
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
):
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

        package_dimensions.model_validate()

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
        active=active == bool_string.TRUE,
        options=option_values,
        accept_zero_inventory_orders=accept_zero_inventory_orders == bool_string.TRUE,
        # TODO convert string to datetime timestamp
        next_refill=int(datetime.now().timestamp()),
        package_dimensions=package_dimensions,
    )


@router.post("", response_model=schema.Variant)
def create_variant(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    variant: Annotated[schema.Variant, Depends(create_variant_form)],
):
    new_variant = crud.create_variant(
        x_shop_id,
        x_livemode,
        variant,
    )
    return new_variant


@router.post("/{variant_id}", response_model=schema.Variant)
def update_variant(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    variant_id: str,
    variant: Annotated[schema.Variant, Depends(create_variant_form)],
):
    updated_variant = crud.update_variant(
        x_shop_id,
        x_livemode,
        variant_id,
        variant,
    )


@router.get("/{variant_id}", response_model=schema.Variant)
def retrieve_variant(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    variant_id: str,
):
    variant = crud.retrieve_variant(
        x_shop_id,
        x_livemode,
        variant_id,
    )
    return variant


@router.get("", response_model=schema.VariantList)
def list_variants(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
):
    variant_list = crud.list_variants(
        x_shop_id,
        x_livemode,
    )
    return variant_list


@router.delete("/{variant_id}", response_model=schema.VariantDelete)
def delete_variant(
    x_shop_id: ShopIDDep,
    x_livemode: LivemodeDep,
    variant_id: str,
):
    deleted_id = crud.delete_variant(
        x_shop_id,
        x_livemode,
        variant_id,
    )
    deleted_variant = schema.VariantDelete(
        id=variant_id,
        deleted=deleted_id is not None,
    )
    return deleted_variant
