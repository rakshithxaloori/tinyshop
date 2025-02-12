from app.invoice.model import Invoice
from app.lib.payment_providers.razorpay import razorpay


def create_razorpay_order(invoice: Invoice):
    razorpay_order = razorpay.order.create(
        {
            "amount": invoice.amount_total,
            "currency": invoice.currency,
            "receipt": invoice.id,
            "notes": {
                "shop": invoice.shop_id,
                "customer": invoice.customer_id,
                "invoice": invoice.id,
            },
        }
    )
    return razorpay_order["id"]
