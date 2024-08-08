from sqlmodel import Session

from app.invoice.model import (
    Invoice,
    InvoiceStatusEnum,
    InvoiceLineItem,
)
from app.checkout.model import Checkout
from app.price.model import Price
from app.price.enum import PriceTypeEnum
from app.lib.enum import PaymentsProviderEnum
from app.invoice.utils.razorpay import create_razorpay_order


def create_one_time_invoice_from_checkout(db: Session, checkout: Checkout):
    # TODO
    # Create an invoice for one-time items
    one_time_price_quantity_list: list[tuple[Price, int]] = []
    for cli in checkout.line_items:
        if cli.price.type == PriceTypeEnum.ONE_TIME:
            one_time_price_quantity_list.append((cli.price, cli.quantity))

    # Create the one-time prices invoice
    amount_subtotal = 0
    amount_discount = 0
    amount_shipping = 0
    amount_tax = 0
    for price, quantity in one_time_price_quantity_list:
        amount_subtotal += price.unit_amount * quantity

    # TODO discount, shipping, tax

    amount_total = amount_subtotal - amount_discount + amount_shipping + amount_tax
    new_one_time_invoice = Invoice(
        amount_paid=0,
        amount_remaining=amount_total,
        amount_subtotal=amount_subtotal,
        amount_discount=amount_discount,
        amount_shipping=amount_shipping,
        amount_tax=amount_tax,
        amount_total=amount_total,
        currency=checkout.currency,
        status=InvoiceStatusEnum.OPEN,
        paid=False,
        provider=checkout.shop.default_payments_provider,
        shop_id=checkout.shop_id,
        livemode=checkout.livemode,
        checkout_id=checkout.id,
        **checkout.customer_address.model_dump(exclude={"id"}),
    )
    db.add(new_one_time_invoice)

    # Create default payments provider invoice
    if checkout.shop.default_payments_provider == PaymentsProviderEnum.RAZORPAY:
        # TODO Create Razorpay Order
        razorpay_order_id = create_razorpay_order(new_one_time_invoice)
        new_one_time_invoice.razorpay_order_id = razorpay_order_id
        # Creates an UPDATE statement
        db.add(new_one_time_invoice)

    # Order Line Items
    for price, quantity in one_time_price_quantity_list:
        # Create an invoice line item
        new_oti_li = InvoiceLineItem(
            invoice_id=new_one_time_invoice.id,
            price_id=price.id,
            quantity=quantity,
            unit_amount=price.unit_amount,
        )
        db.add(new_oti_li)


def create_subscriptions_invoices(db: Session, checkout: Checkout):
    # TODO
    # Create an invoice for one-time items
    one_time_price_quantity_list: list[tuple[Price, int]] = []
    for cli in checkout.line_items:
        if cli.price.type == PriceTypeEnum.ONE_TIME:
            one_time_price_quantity_list.append((cli.price, cli.quantity))

    # Create the one-time prices invoice
    amount_subtotal = 0
    amount_discount = 0
    amount_shipping = 0
    amount_tax = 0
    for price, quantity in one_time_price_quantity_list:
        amount_subtotal += price.unit_amount * quantity

    # TODO discount, shipping, tax

    amount_total = amount_subtotal - amount_discount + amount_shipping + amount_tax
    new_one_time_invoice = Invoice(
        amount_paid=0,
        amount_remaining=amount_total,
        amount_subtotal=amount_subtotal,
        amount_discount=amount_discount,
        amount_shipping=amount_shipping,
        amount_tax=amount_tax,
        amount_total=amount_total,
        currency=checkout.currency,
        status=InvoiceStatusEnum.OPEN,
        paid=False,
        provider=checkout.shop.default_payments_provider,
        shop_id=checkout.shop_id,
        livemode=checkout.livemode,
        checkout_id=checkout.id,
    )
    db.add(new_one_time_invoice)
    for price, quantity in one_time_price_quantity_list:
        # Create an invoice line item
        new_oti_li = InvoiceLineItem(
            invoice_id=new_one_time_invoice.id,
            price_id=price.id,
            quantity=quantity,
            unit_amount=price.unit_amount,
        )
        db.add(new_oti_li)

    # Create default payments provider invoice
    # Create Razorpay Order

    # Create an invoice for each subscription
