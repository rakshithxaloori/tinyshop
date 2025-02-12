from app.order.model import Order
from app.order import schema


def pydantify_orders(rows: list[Order]) -> list[schema.Order]:
    orders: list[schema.Order] = []
    for order_ins in rows:
        orders.append(
            schema.Order(
                **order_ins.model_dump(exclude={"invoice", "customer", "line_items"}),
                customer=order_ins.customer_id,
                invoice=order_ins.invoice_id,
                line_items=[
                    schema.OrderLineItem(
                        **line_item.model_dump(exclude={"price"}),
                        price=line_item.price_id
                    )
                    for line_item in order_ins.line_items
                ]
            )
        )
    return orders
