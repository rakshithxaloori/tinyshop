from sqlmodel import Session, select

from customer.model import Customer
from checkout.model import Checkout
from invoice.model import Invoice, InvoiceCustomerAddress, InvoiceStatusEnum
from invoice import schema
from invoice.utils import pydantify_invoices
from lib.session import update_instance


def create_invoice(
    shop_id: str,
    livemode: bool,
    invoice: schema.InvoiceCreate,
    db: Session,
) -> schema.Invoice | None:
    try:
        invoice_data = invoice.model_dump(exclude={"checkout", "subscriptions"})
        # TODO subscriptions
        checkout_res = db.exec(
            select(Checkout)
            .where(Checkout.shop_id == shop_id)
            .where(Checkout.livemode == livemode)
            .where(Checkout.id == invoice.checkout)
        )
        checkout = checkout_res.one()
        address_data = checkout.customer_address.model_dump()
        new_invoice = Invoice(
            shop_id=shop_id,
            livemode=livemode,
            customer_id=checkout.customer_id,
            checkout_id=checkout.id,
            # amount_paid
            amount_subtotal=checkout.amount_subtotal,
            amount_total=checkout.amount_total,
            amount_remaining=checkout.amount_total,
            amount_shipping=checkout.amount_shipping,
            amount_tax=checkout.amount_tax,
            amount_discount=checkout.amount_discount,
            currency=checkout.line_items[0].price.currency,  # TODO better way?
            paid=False,
            **invoice_data,
        )
        db.add(new_invoice)
        new_in_cus_addr = InvoiceCustomerAddress(
            invoice_id=new_invoice.id,
            **address_data,
        )
        db.add(new_in_cus_addr)

        db.commit()
        db.refresh(new_invoice)
        db.refresh(new_in_cus_addr)
        py_invoices = pydantify_invoices([new_invoice])
        return py_invoices.pop()
    except Exception as e:
        print("EXCEPTION create_invoice:", e)
        return None


def update_invoice(
    shop_id: str,
    livemode: bool,
    invoice_id: str,
    invoice: schema.InvoiceUpdate,
    db: Session,
) -> schema.Invoice | None:
    try:
        data = invoice.model_dump(exclude_none=True)

        invoice_res = db.exec(
            select(Invoice)
            .where(Invoice.shop_id == shop_id)
            .where(Invoice.livemode == livemode)
            .where(Invoice.id == invoice_id)
        )
        invoice_ins = invoice_res.one()
        update_instance(db, data, invoice_ins)
        invoice_ins.paid = invoice_ins.amount_remaining == 0
        db.add(invoice_ins)
        db.commit()
        db.refresh(invoice_ins)
        py_invoices = pydantify_invoices([invoice_ins])
        return py_invoices.pop()

    except Exception as e:
        print("EXCEPTION update_invoice:", e)
        return None


def retrieve_invoice(
    shop_id: str,
    livemode: bool,
    invoice_id: str,
    db: Session,
) -> schema.Invoice | None:
    try:
        res = db.exec(
            select(Invoice)
            .where(Invoice.shop_id == shop_id)
            .where(Invoice.livemode == livemode)
            .where(Invoice.id == invoice_id)
        )
        invoice_ins = res.one()
        py_invoices = pydantify_invoices([invoice_ins])
        return py_invoices.pop()
    except Exception as e:
        print("EXCEPTION retrieve_invoice:", e)
        return None


def list_invoices(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.InvoiceList:
    results = db.exec(
        select(Invoice)
        .where(Invoice.shop_id == shop_id)
        .where(Invoice.livemode == livemode)
        .offset(skip)
        .limit(limit)
    )
    invoice_rows = list(results.all())
    invoices = pydantify_invoices(invoice_rows)
    return schema.InvoiceList(
        has_more=False,  # TODO
        data=invoices,
    )


def delete_invoice(
    shop_id: str,
    livemode: bool,
    invoice_id: str,
    db: Session,
) -> str | None:
    try:
        res = db.exec(
            select(Invoice)
            .where(Invoice.shop_id == shop_id)
            .where(Invoice.livemode == livemode)
            .where(Invoice.id == invoice_id)
        )
        invoice = res.one()
        db.delete(invoice)
        db.commit()
        return invoice.id
    except Exception as e:
        print("EXCEPTION delete_invoice:", e)
        return None
