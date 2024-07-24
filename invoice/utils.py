from invoice.model import Invoice
from invoice import schema


def pydantify_invoices(rows: list[Invoice]) -> list[schema.Invoice]:
    invoices: list[schema.Invoice] = []
    for invoice_ins in rows:
        invoices.append(
            schema.Invoice(
                **invoice_ins.model_dump(
                    exclude={
                        "customer",
                        "checkout",
                        "customer_address",
                        # TODO subscriptions
                    }
                ),
                customer=invoice_ins.customer_id,
                checkout=invoice_ins.checkout_id,
                customer_address=schema.InvoiceCustomerAddress(
                    **invoice_ins.customer_address.model_dump(
                        exclude={"created", "updated"}
                    )
                )
            )
        )
    return invoices
