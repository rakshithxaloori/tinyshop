from discount.model import Discount, DiscountTypeEnum
from discount import schema
from customer import schema as cus_schema
from product import schema as prod_schema
from product.model import Product
from variant import schema as var_schema

EXPAND_LIMIT = 20


def pydantify_discounts(rows: list[(Discount)]) -> list[schema.Discount]:
    discounts: list[schema.Discount] = []
    for discount_ins in rows:
        discount_config = None
        if discount_ins.type == DiscountTypeEnum.OFF_PRODUCT:
            discount_config = schema.DiscountConfig(
                off_product=schema.OffProduct(
                    **discount_ins.config.off_product.model_dump(
                        exclude={"created", "updated", "products"}
                    ),
                    products=_get_discount_products(
                        discount_ins.id,
                        list(discount_ins.config.off_product.products[:EXPAND_LIMIT]),
                    ),
                )
            )
        elif discount_ins.type == DiscountTypeEnum.OFF_ORDER:
            discount_config = schema.DiscountConfig(
                off_order=schema.OffOrder(
                    **discount_ins.config.off_order.model_dump(
                        exclude={"created", "updated"}
                    ),
                )
            )
        elif discount_ins.type == DiscountTypeEnum.SHIPPING:
            discount_config = schema.DiscountConfig(
                shipping=schema.Shipping(
                    **discount_ins.config.shipping.model_dump(
                        exclude={"created", "updated"}
                    ),
                )
            )
        elif discount_ins.type == DiscountTypeEnum.BUY_X_GET_Y:
            print("discount_ins.config.buy_x_get_y", discount_ins.config)
            variant_ins = discount_ins.config.buy_x_get_y.variant_get
            discount_config = schema.DiscountConfig(
                buy_x_get_y=schema.BuyXGetY(
                    **discount_ins.config.buy_x_get_y.model_dump(
                        exclude={"created", "updated", "products_buy", "variant_get"}
                    ),
                    products_buy=_get_discount_products(
                        discount_ins.id,
                        list(
                            discount_ins.config.buy_x_get_y.products_buy[:EXPAND_LIMIT]
                        ),
                    ),
                    # variant_get=var_schema.Variant(
                    #     **variant_ins.model_dump(exclude={"created", "updated"}),
                    #     created=int(variant_ins.created.timestamp()),
                    #     updated=int(variant_ins.updated.timestamp()),
                    # ),
                    variant_get=variant_ins.id,
                )
            )
        discount_py = schema.Discount(
            **discount_ins.model_dump(exclude={"created", "updated", "config"}),
            created=int(discount_ins.created.timestamp()),
            updated=int(discount_ins.updated.timestamp()),
            customers=schema.DiscountCustomersList(
                # data=[
                #     cus_schema.Customer(
                #         **cus.customer.model_dump(exclude={"created", "updated"}),
                #         created=int(cus.created.timestamp()),
                #         updated=int(cus.updated.timestamp()),
                #     )
                #     for cus in discount_ins.customer_links[:EXPAND_LIMIT]
                # ],
                data=[
                    cd_link.customer_id
                    for cd_link in discount_ins.customer_links[:EXPAND_LIMIT]
                ],
                url=f"/v1/discounts/{discount_ins.id}/customers",
                has_more=False,  # TODO
            ),
            config=discount_config,
        )

        discounts.append(discount_py)

    return discounts


def _get_discount_products(
    discount_id: str, products: list[Product]
) -> schema.DiscountProductsList:
    return schema.DiscountProductsList(
        data=[
            # prod_schema.Product(
            #     **prod.model_dump(
            #         exclude={
            #             "created",
            #             "updated",
            #             "options",
            #             "variants",
            #         }
            #     ),
            #     created=int(prod.created.timestamp()),
            #     updated=int(prod.updated.timestamp()),
            # )
            prod.id
            for prod in products[:EXPAND_LIMIT]
        ],
        url=f"/v1/discounts/{discount_id}/products",
        has_more=False,  # TODO
    )
