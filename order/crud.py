from sqlmodel import Session, select


from order.model import Order, OrderTypeEnum, OrderStatusEnum, OrderLineItem
from customer.model import Customer
from invoice.model import Invoice
from price.model import Price
from order.utils import pydantify_orders
from lib.session import update_instance
from order import schema


def _create_order_line_items(
    db: Session,
    livemode: bool,
    prices: list[Price],
    order: Order,
    quantities_dict: dict[str, int],
):
    # Create line items
    for price_ins in prices:
        new_oli = OrderLineItem(
            livemode=livemode,
            order_id=order.id,
            price_id=price_ins.id,
            quantity=quantities_dict[price_ins.id],
            unit_amount=price_ins.unit_amount,
        )
        db.add(new_oli)


def create_order(
    shop_id: str,
    livemode: bool,
    order: schema.OrderCreate,
    db: Session,
) -> schema.OrderList | None:
    try:
        customer_res = db.exec(
            select(Customer.id)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == order.customer)
        )
        customer_id = customer_res.one()

        invoice_id = None
        # Create seperate orders for each type
        preorder_prices: list[Price] = []
        deferred_prices: list[Price] = []
        normal_prices: list[Price] = []

        # Prices Dict
        quantities_dict = {
            line_item.price: line_item.quantity for line_item in order.line_items
        }

        prices_res = db.exec(
            select(Price)
            .where(Price.shop_id == shop_id)
            .where(Price.livemode == livemode)
            .where(Price.id.in_([line_item.price for line_item in order.line_items]))
        )
        prices_ins = prices_res.all()
        for price_ins in prices_ins:
            if price_ins.variant.product.preorder:
                preorder_prices.append(price_ins)
            # elif inventory is zero, add it to deferred
            is_inventory_available = False
            for inventory in price_ins.variant.inventories:
                if inventory.quantity > 0:
                    is_inventory_available = True
                    break
            if not is_inventory_available:
                deferred_prices.append(price_ins)
            else:
                normal_prices.append(price_ins)
        if order.invoice:
            invoice_res = db.exec(
                select(Invoice.id)
                .where(Invoice.shop_id == shop_id)
                .where(Invoice.livemode == livemode)
                .where(Invoice.id == order.invoice)
            )
            invoice_id = invoice_res.one()

        new_preorder_order = None
        new_deferred_order = None
        new_normal_order = None
        # TODO order numbers
        if len(preorder_prices) > 0:
            new_preorder_order = Order(
                shop_id=shop_id,
                livemode=livemode,
                number=1000,
                customer_id=customer_id,
                invoice_id=invoice_id,
                type=OrderTypeEnum.PREORDER,
                status=OrderStatusEnum.REQUIRES_INVENTORY,
            )
            db.add(new_preorder_order)
            _create_order_line_items(
                db, livemode, preorder_prices, new_preorder_order, quantities_dict
            )

        if len(deferred_prices) > 0:
            new_deferred_order = Order(
                shop_id=shop_id,
                livemode=livemode,
                number=1000,
                customer_id=customer_id,
                invoice_id=invoice_id,
                type=OrderTypeEnum.DEFERRED,
                status=OrderStatusEnum.REQUIRES_INVENTORY,
            )
            db.add(new_deferred_order)
            _create_order_line_items(
                db, livemode, deferred_prices, new_deferred_order, quantities_dict
            )

        if len(normal_prices) > 0:
            new_normal_order = Order(
                shop_id=shop_id,
                livemode=livemode,
                number=1000,
                customer_id=customer_id,
                invoice_id=invoice_id,
                type=OrderTypeEnum.NORMAL,
                status=OrderStatusEnum.REQUIRES_SHIPPING,
            )
            db.add(new_normal_order)
            _create_order_line_items(
                db, livemode, normal_prices, new_normal_order, quantities_dict
            )

        db.commit()
        all_orders: list[Order] = []
        for new_order in [new_preorder_order, new_deferred_order, new_normal_order]:
            if new_order:
                db.refresh(new_order)
                all_orders.append(new_order)
        py_orders = pydantify_orders(all_orders)
        return schema.OrderList(
            data=py_orders,
            has_more=False,
        )
    except Exception as e:
        print("EXCEPTION create_order:", e)
        return None


def update_order(
    shop_id: str,
    livemode: bool,
    order_id: str,
    order: schema.OrderUpdate,
    db: Session,
) -> schema.Order | None:
    try:
        data = order.model_dump(exclude_none=True)

        order_res = db.exec(
            select(Order)
            .where(Order.shop_id == shop_id)
            .where(Order.livemode == livemode)
            .where(Order.id == order_id)
        )
        order_ins = order_res.one()
        update_instance(db, data, order_ins)
        db.commit()
        db.refresh(order_ins)
        py_orders = pydantify_orders([order_ins])
        return py_orders.pop()

    except Exception as e:
        print("EXCEPTION update_order:", e)
        return None


def retrieve_order(
    shop_id: str,
    livemode: bool,
    order_id: str,
    db: Session,
) -> schema.Order | None:
    try:
        order_res = db.exec(
            select(Order)
            .where(Order.shop_id == shop_id)
            .where(Order.livemode == livemode)
            .where(Order.id == order_id)
        )
        order_ins = order_res.one()
        py_orders = pydantify_orders([order_ins])
        return py_orders.pop()
    except Exception as e:
        print("EXCEPTION retrieve_order:", e)
        return None


def list_orders(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.OrderList:
    results = db.exec(
        select(Order)
        .where(Order.shop_id == shop_id)
        .where(Order.livemode == livemode)
        .offset(skip)
        .limit(limit)
    )
    rows = list(results.all())
    orders = pydantify_orders(rows)
    return schema.OrderList(has_more=False, data=orders)  # TODO


def delete_order(
    shop_id: str,
    livemode: bool,
    order_id: str,
    db: Session,
) -> schema.OrderDelete | None:
    try:
        order_res = db.exec(
            select(Order)
            .where(Order.shop_id == shop_id)
            .where(Order.livemode == livemode)
            .where(Order.id == order_id)
        )
        order_ins = order_res.one()
        db.delete(order_ins)
        db.commit()
        return schema.OrderDelete(
            id=order_ins.id,
            deleted=True,
        )
    except Exception as e:
        print("EXCEPTION retrieve_order:", e)
        return schema.OrderDelete(
            id=order_id,
            deleted=False,
        )
