from invoice.model import Invoice
from lib.payment_providers.razorpay import razorpay


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
    invoice.razorpay_order_id = razorpay_order.id
