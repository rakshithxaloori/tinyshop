from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Form


from discount import schema
from discount.model import DiscountTypeEnum


def create_discount_form(
    discount_type: Annotated[str, Form(alias="type")],
    code: Annotated[str, Form()],
    active: Annotated[str, Form()],
    expires_at: Annotated[str | None, Form()] = None,
    applies_max: Annotated[int | None, Form()] = None,
    customers: Annotated[list[str], Form(alias="customers[]")] = [],
    config_off_product_quantity_min: Annotated[
        int | None, Form(alias="config[off_product][quantity_min]")
    ] = None,
    config_off_product_amount_off: Annotated[
        int | None, Form(alias="config[off_product][amount_off]")
    ] = None,
    config_off_product_percentage_off: Annotated[
        int | None, Form(alias="config[off_product][percentage_off]")
    ] = None,
    config_off_product_products: Annotated[
        list[str], Form(alias="config[off_product][products][]")
    ] = [],
    config_off_order_quantity_min: Annotated[
        int | None, Form(alias="config[off_order][quantity_min]")
    ] = None,
    config_off_order_amount_min: Annotated[
        int | None, Form(alias="config[off_order][amount_min]")
    ] = None,
    config_off_order_amount_off: Annotated[
        int | None, Form(alias="config[off_order][amount_off]")
    ] = None,
    config_off_order_percentage_off: Annotated[
        int | None, Form(alias="config[off_order][percentage_off]")
    ] = None,
    config_shipping_quantity_min: Annotated[
        int | None, Form(alias="config[shipping][quantity_min]")
    ] = None,
    config_shipping_amount_min: Annotated[
        int | None, Form(alias="config[shipping][amount_min]")
    ] = None,
    config_shipping_amount_off: Annotated[
        int | None, Form(alias="config[shipping][amount_off]")
    ] = None,
    config_shipping_percentage_off: Annotated[
        int | None, Form(alias="config[shipping][percentage_off]")
    ] = None,
    config_buy_x_get_y_quantity_min: Annotated[
        int | None, Form(alias="config[buy_x_get_y][quantity_min]")
    ] = None,
    config_buy_x_get_y_amount_min: Annotated[
        int | None, Form(alias="config[buy_x_get_y][amount_min]")
    ] = None,
    config_buy_x_get_y_quantity_get: Annotated[
        int | None, Form(alias="config[buy_x_get_y][quantity_get]")
    ] = None,
    config_buy_x_get_y_products_buy: Annotated[
        list[str], Form(alias="config[buy_x_get_y][products_buy][]")
    ] = [],
    config_buy_x_get_y_variant_get: Annotated[
        str | None, Form(alias="config[buy_x_get_y][variant_get]")
    ] = None,
) -> schema.DiscountCreate:
    # TODO validation
    # BOTH amount_off and percentage_off can't be there - XOR validation
    config = None
    if discount_type == DiscountTypeEnum.OFF_PRODUCT:
        config = schema.DiscountConfig(
            off_product=schema.OffProduct(
                quantity_min=config_off_product_quantity_min,
                amount_off=config_off_product_amount_off,
                percentage_off=config_off_product_percentage_off,
                products=config_off_product_products,
            )
        )

    if discount_type == DiscountTypeEnum.OFF_ORDER:
        config = schema.DiscountConfig(
            off_order=schema.OffOrder(
                quantity_min=config_off_order_quantity_min,
                amount_min=config_off_order_amount_min,
                amount_off=config_off_order_amount_off,
                percentage_off=config_off_order_percentage_off,
            )
        )

    if discount_type == DiscountTypeEnum.SHIPPING:
        config = schema.DiscountConfig(
            shipping=schema.Shipping(
                quantity_min=config_shipping_quantity_min,
                amount_min=config_shipping_amount_min,
                amount_off=config_shipping_amount_off,
                percentage_off=config_shipping_percentage_off,
            )
        )

    if discount_type == DiscountTypeEnum.BUY_X_GET_Y:
        # TODO if variant_get_id is None, raise error
        config = schema.DiscountConfig(
            buy_x_get_y=schema.BuyXGetY(
                quantity_min=config_buy_x_get_y_quantity_min,
                amount_min=config_buy_x_get_y_amount_min,
                quantity_get=config_buy_x_get_y_quantity_get,
                products_buy=config_buy_x_get_y_products_buy,
                variant_get=config_buy_x_get_y_variant_get,
            )
        )

    return schema.DiscountCreate(
        type=discount_type,
        code=code,
        active=active == "true",
        expires_at=datetime.now() + timedelta(days=30),  # TODO
        applies_max=applies_max,
        customers=customers,
        config=config,
    )

    # TODO raise error


def update_discount_form(
    active: Annotated[str, Form()],
    expires_at: Annotated[str | None, Form()] = None,
    applies_max: Annotated[int | None, Form()] = None,
    customers_add: Annotated[list[str], Form(alias="customers[add][]")] = [],
    customers_remove: Annotated[list[str], Form(alias="customers[remove][]")] = [],
    config_off_product_quantity_min: Annotated[
        int | None, Form(alias="config[off_product][quantity_min]")
    ] = None,
    config_off_product_amount_off: Annotated[
        int | None, Form(alias="config[off_product][amount_off]")
    ] = None,
    config_off_product_percentage_off: Annotated[
        int | None, Form(alias="config[off_product][percentage_off]")
    ] = None,
    config_off_product_products_add: Annotated[
        list[str], Form(alias="config[off_product][products][add][]")
    ] = [],
    config_off_product_products_remove: Annotated[
        list[str], Form(alias="config[off_product][products][remove][]")
    ] = [],
    config_off_order_quantity_min: Annotated[
        int | None, Form(alias="config[off_order][quantity_min]")
    ] = None,
    config_off_order_amount_min: Annotated[
        int | None, Form(alias="config[off_order][amount_min]")
    ] = None,
    config_off_order_amount_off: Annotated[
        int | None, Form(alias="config[off_order][amount_off]")
    ] = None,
    config_off_order_percentage_off: Annotated[
        int | None, Form(alias="config[off_order][percentage_off]")
    ] = None,
    config_shipping_quantity_min: Annotated[
        int | None, Form(alias="config[shipping][quantity_min]")
    ] = None,
    config_shipping_amount_min: Annotated[
        int | None, Form(alias="config[shipping][amount_min]")
    ] = None,
    config_shipping_amount_off: Annotated[
        int | None, Form(alias="config[shipping][amount_off]")
    ] = None,
    config_shipping_percentage_off: Annotated[
        int | None, Form(alias="config[shipping][percentage_off]")
    ] = None,
    config_buy_x_get_y_quantity_min: Annotated[
        int | None, Form(alias="config[buy_x_get_y][quantity_min]")
    ] = None,
    config_buy_x_get_y_amount_min: Annotated[
        int | None, Form(alias="config[buy_x_get_y][amount_min]")
    ] = None,
    config_buy_x_get_y_quantity_get: Annotated[
        int | None, Form(alias="config[buy_x_get_y][quantity_get]")
    ] = None,
    config_buy_x_get_y_products_buy_add: Annotated[
        list[str], Form(alias="config[buy_x_get_y][products_buy][add][]")
    ] = [],
    config_buy_x_get_y_products_buy_remove: Annotated[
        list[str], Form(alias="config[buy_x_get_y][products_buy][remove][]")
    ] = [],
    config_buy_x_get_y_variant_get: Annotated[
        str | None, Form(alias="config[buy_x_get_y][variant_get]")
    ] = None,
) -> schema.DiscountUpdate:
    return schema.DiscountUpdate(
        active=active == "true" if active else None,
        expires_at=datetime.now() + timedelta(days=30),  # TODO
        applies_max=applies_max,
        customers=schema.DiscountUpdateCustomers(
            add=customers_add,
            remove=customers_remove,
        ),
        config=schema.DiscountConfig(
            off_product=schema.OffProductUpdate(
                quantity_min=config_off_product_quantity_min,
                amount_off=config_off_product_amount_off,
                percentage_off=config_off_product_percentage_off,
                products=schema.OffProductUpdateProducts(
                    add=config_off_product_products_add,
                    remove=config_off_product_products_remove,
                ),
            ),
            off_order=schema.OffOrder(
                quantity_min=config_off_order_quantity_min,
                amount_min=config_off_order_amount_min,
                amount_off=config_off_order_amount_off,
                percentage_off=config_off_order_percentage_off,
            ),
            shipping=schema.Shipping(
                quantity_min=config_shipping_quantity_min,
                amount_min=config_shipping_amount_min,
                amount_off=config_shipping_amount_off,
                percentage_off=config_shipping_percentage_off,
            ),
            buy_x_get_y=schema.BuyXGetYUpdate(
                quantity_min=config_buy_x_get_y_quantity_min,
                amount_min=config_buy_x_get_y_amount_min,
                quantity_get=config_buy_x_get_y_quantity_get,
                products_buy=schema.BuyXGetYUpdateProducts(
                    add=config_buy_x_get_y_products_buy_add,
                    remove=config_buy_x_get_y_products_buy_remove,
                ),
                variant_get=config_buy_x_get_y_variant_get,
            ),
        ),
    )
