from sqlmodel import Session, select

from discount.model import (
    Discount,
    DiscountTypeEnum,
    DiscountConfig,
    DiscountConfigOffProduct,
    DiscountConfigOffOrder,
    DiscountConfigShipping,
    DiscountConfigBuyXGetY,
)
from discount import schema
from customer.model import Customer
from product.model import Product
from variant.model import Variant
from discount.utils import pydantify_discounts
from lib.session import update_instance
from lib.many_to_many_tables import DiscountCustomerLink


def create_discount(
    shop_id: str,
    livemode: bool,
    discount: schema.DiscountCreate,
    db: Session,
) -> schema.Discount | None:
    try:
        discount_data = discount.model_dump(exclude={"customers", "config"})

        new_discount = Discount(
            shop_id=shop_id,
            livemode=livemode,
            **discount_data,
        )

        if discount.customers:
            cus_results = db.exec(
                select(Customer.id)
                .where(Customer.shop_id == shop_id)
                .where(Customer.livemode == livemode)
                .where(Customer.id.in_(discount.customers))
            )
            cus_ids = list(cus_results.all())
            for cus_id in cus_ids:
                new_dc_link = DiscountCustomerLink(
                    livemode=livemode,
                    discount_id=new_discount.id,
                    customer_id=cus_id,
                )
                new_discount.customer_links.append(new_dc_link)
                db.add(new_dc_link)

        db.add(new_discount)

        new_config = DiscountConfig(
            discount_id=new_discount.id,
            livemode=livemode,
        )
        db.add(new_config)
        new_discount_specific = None
        if discount.type == DiscountTypeEnum.OFF_PRODUCT:
            products_list = discount.config.off_product.products
            products_ins = []
            if products_list and len(products_list) > 0:
                products_res = db.exec(
                    select(Product)
                    .where(Product.shop_id == shop_id)
                    .where(Product.livemode == livemode)
                    .where(Product.id.in_(products_list))
                )
                products_ins = list(products_res.all())

            new_discount_specific = DiscountConfigOffProduct(
                livemode=livemode,
                config_id=new_config.id,
                products=products_ins,
                **discount.config.off_product.model_dump(exclude={"products"}),
            )

        elif discount.type == DiscountTypeEnum.OFF_ORDER:
            new_discount_specific = DiscountConfigOffOrder(
                livemode=livemode,
                config_id=new_config.id,
                **discount.config.off_order.model_dump(),
            )
        elif discount.type == DiscountTypeEnum.SHIPPING:
            new_discount_specific = DiscountConfigShipping(
                livemode=livemode,
                config_id=new_config.id,
                **discount.config.shipping.model_dump(),
            )
        elif discount.type == DiscountTypeEnum.BUY_X_GET_Y:
            products_buy_ids = discount.config.buy_x_get_y.products_buy
            variant_get_id = discount.config.buy_x_get_y.variant_get
            products_ins = []
            variant_ins = None

            if products_buy_ids and len(products_buy_ids) > 0:
                products_res = db.exec(
                    select(Product)
                    .where(Product.shop_id == shop_id)
                    .where(Product.livemode == livemode)
                    .where(Product.id.in_(products_buy_ids))
                )
                products_ins = list(products_res.all())
            if variant_get_id:
                variant_res = db.exec(
                    select(Variant)
                    .where(Variant.shop_id == shop_id)
                    .where(Variant.livemode == livemode)
                    .where(Variant.id == discount.config.buy_x_get_y.variant_get)
                )
                variant_ins = variant_res.one()

            new_discount_specific = DiscountConfigBuyXGetY(
                livemode=livemode,
                config_id=new_config.id,
                products_buy=products_ins,
                variant_get=variant_ins,
                **discount.config.buy_x_get_y.model_dump(
                    exclude={"products_buy", "variant_get"}
                ),
            )

        db.add(new_discount_specific)

        db.commit()
        db.refresh(new_discount)
        db.refresh(new_config)
        db.refresh(new_discount_specific)

        py_discounts = pydantify_discounts([new_discount])
        return py_discounts.pop()

    except Exception as e:
        print("EXCEPTION create_discount:", e)
        return None


def update_discount(
    shop_id: str,
    livemode: bool,
    discount_id: str,
    discount: schema.DiscountUpdate,
    db: Session,
) -> schema.Discount | None:
    try:
        data = discount.model_dump(exclude_none=True, exclude={"customers", "config"})
        statement = (
            select(Discount)
            .where(Discount.shop_id == shop_id)
            .where(Discount.livemode == livemode)
            .where(Discount.id == discount_id)
        )
        results = db.exec(statement)
        discount_ins = results.one()

        update_instance(db, data, discount_ins)

        customers = discount.customers
        if customers:
            if customers.add:
                # Add these customers
                cus_results = db.exec(
                    select(Customer.id)
                    .where(Customer.shop_id == shop_id)
                    .where(Customer.livemode == livemode)
                    .where(Customer.id.in_(customers.add))
                )
                cus_ids = list(cus_results.all())
                for cus_id in cus_ids:
                    new_dc_link = DiscountCustomerLink(
                        livemode=livemode,
                        discount_id=discount_ins.id,
                        customer_id=cus_id,
                    )
                    discount_ins.customer_links.append(new_dc_link)
                    db.add(new_dc_link)
            if customers.remove:
                # Remove these customers
                dc_links_res = db.exec(
                    select(DiscountCustomerLink)
                    .where(DiscountCustomerLink.livemode == livemode)
                    .where(DiscountCustomerLink.discount_id == discount_ins.id)
                    .where(DiscountCustomerLink.customer_id.in_(customers.remove))
                )
                dc_links = dc_links_res.all()
                for dc_link in dc_links:
                    db.delete(dc_link)
            db.add(discount_ins)

        if discount.config:
            if discount_ins.type == DiscountTypeEnum.OFF_PRODUCT:
                off_p = discount.config.off_product
                off_p_data = off_p.model_dump(exclude_none=True, exclude={"products"})
                if off_p.products.add:
                    products_res = db.exec(
                        select(Product)
                        .where(Product.shop_id == shop_id)
                        .where(Product.livemode == livemode)
                        .where(Product.id.in_(off_p.products.add))
                    )
                    products_ins = list(products_res.all())
                    for p_ins in products_ins:
                        discount_ins.config.off_product.products.append(p_ins)
                if off_p.products.remove:
                    products_res = db.exec(
                        select(Product)
                        .where(Product.shop_id == shop_id)
                        .where(Product.livemode == livemode)
                        .where(Product.id.in_(off_p.products.remove))
                    )
                    products_ins = list(products_res.all())
                    for p_ins in products_ins:
                        discount_ins.config.off_product.products.remove(p_ins)
                update_instance(
                    db,
                    off_p_data,
                    discount_ins.config.off_product,
                )
            elif discount_ins.type == DiscountTypeEnum.OFF_ORDER:
                update_instance(
                    db,
                    discount.config.off_order.model_dump(exclude_none=True),
                    discount_ins.config.off_order,
                )
            elif discount_ins.type == DiscountTypeEnum.SHIPPING:
                update_instance(
                    db,
                    discount.config.shipping.model_dump(exclude_none=True),
                    discount_ins.config.shipping,
                )
            elif discount_ins.type == DiscountTypeEnum.BUY_X_GET_Y:
                bxgy = discount.config.buy_x_get_y
                bxgy_data = bxgy.model_dump(
                    exclude_none=True, exclude={"products_buy", "variant_get"}
                )
                if bxgy.products_buy.add:
                    products_res = db.exec(
                        select(Product)
                        .where(Product.shop_id == shop_id)
                        .where(Product.livemode == livemode)
                        .where(Product.id.in_(bxgy.products_buy.add))
                    )
                    products_ins = list(products_res.all())
                    for p_ins in products_ins:
                        discount_ins.config.buy_x_get_y.products_buy.append(p_ins)
                if bxgy.products_buy.remove:
                    products_res = db.exec(
                        select(Product)
                        .where(Product.shop_id == shop_id)
                        .where(Product.livemode == livemode)
                        .where(Product.id.in_(bxgy.products_buy.remove))
                    )
                    products_ins = list(products_res.all())
                    for p_ins in products_ins:
                        discount_ins.config.buy_x_get_y.products_buy.remove(p_ins)

                if bxgy.variant_get:
                    variant_res = db.exec(
                        select(Variant)
                        .where(Variant.shop_id == shop_id)
                        .where(Variant.livemode == livemode)
                        .where(Variant.id == bxgy.variant_get)
                    )
                    variant_ins = variant_res.one()
                    discount_ins.config.buy_x_get_y.variant_get = variant_ins

                update_instance(
                    db,
                    bxgy_data,
                    discount_ins.config.buy_x_get_y,
                )

        db.commit()
        db.refresh(discount_ins)
        py_discounts = pydantify_discounts([discount_ins])
        return py_discounts.pop()

    except Exception as e:
        print("EXCEPTION update_discount:", e)
        return None


def retrieve_discount(
    shop_id: str,
    livemode: bool,
    discount_id: str,
    db: Session,
) -> schema.Discount | None:
    try:
        query = (
            select(Discount)
            .where(Discount.shop_id == shop_id)
            .where(Discount.livemode == livemode)
            .where(Discount.id == discount_id)
        )

        result = db.exec(query)
        discount = result.one()
        py_discounts = pydantify_discounts([discount])
        return py_discounts.pop()
    except Exception as e:
        print("EXCEPTION retrieve_discount:", e)
        return None


def list_discounts(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.DiscountList:
    subquery = select(Discount.id).offset(skip).limit(limit)

    results = db.exec(
        select(Discount)
        .where(Discount.shop_id == shop_id)
        .where(Discount.livemode == livemode)
        .where(Discount.id.in_(subquery))
    )
    all_rows = list(results.all())
    discounts = pydantify_discounts(all_rows)
    return schema.DiscountList(
        has_more=False,
        data=discounts,
    )


def delete_discount(
    shop_id: str,
    livemode: bool,
    discount_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Discount)
            .where(Discount.shop_id == shop_id)
            .where(Discount.livemode == livemode)
            .where(Discount.id == discount_id)
        )
        discount = results.one()
        db.delete(discount)
        db.commit()
        return discount.id
    except Exception as e:
        print("EXCEPTION delete_discount:", e)
        return None
