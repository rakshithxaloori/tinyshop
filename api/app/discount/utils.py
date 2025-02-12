from app.discount.model import Discount, DiscountTypeEnum
from app.discount import schema
from app.product.model import Product
from app.lib.limit import LIST_LIMIT_COUNT


def pydantify_discounts(rows: list[Discount]) -> list[schema.Discount]:
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
                        list(
                            discount_ins.config.off_product.products[:LIST_LIMIT_COUNT]
                        ),
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
            variant_ins = discount_ins.config.buy_x_get_y.variant_get
            discount_config = schema.DiscountConfig(
                buy_x_get_y=schema.BuyXGetY(
                    **discount_ins.config.buy_x_get_y.model_dump(
                        exclude={"created", "updated", "products_buy", "variant_get"}
                    ),
                    products_buy=_get_discount_products(
                        discount_ins.id,
                        list(
                            discount_ins.config.buy_x_get_y.products_buy[
                                :LIST_LIMIT_COUNT
                            ]
                        ),
                    ),
                    variant_get=variant_ins.id,
                )
            )
        discount_py = schema.Discount(
            **discount_ins.model_dump(exclude={"config"}),
            customers=schema.DiscountCustomersList(
                data=[
                    cd_link.customer_id
                    for cd_link in discount_ins.customer_links[:LIST_LIMIT_COUNT]
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
        data=[prod.id for prod in products[:LIST_LIMIT_COUNT]],
        url=f"/v1/discounts/{discount_id}/products",
        has_more=False,  # TODO
    )
