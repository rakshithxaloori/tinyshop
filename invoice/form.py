from typing import Annotated
from fastapi import Form


from invoice import schema


def create_invoice_form(
    amount_paid: Annotated[int, Form()],
    due_date: Annotated[int, Form()],
    status: Annotated[str, Form()],
    checkout: Annotated[str | None, Form()] = None,
    subscriptions: Annotated[list[str], Form(alias="subscriptions[]")] = [],
) -> schema.InvoiceCreate:
    return schema.InvoiceCreate(
        amount_paid=amount_paid,
        due_date=due_date,
        status=status,
        checkout=checkout,
        subscriptions=subscriptions,
    )


def update_invoice_form(
    attempt_count: Annotated[int | None, Form()] = None,
    attempted: Annotated[str | None, Form()] = None,
    amount_paid: Annotated[int | None, Form()] = None,
    amount_remaining: Annotated[int | None, Form()] = None,
    due_date: Annotated[int | None, Form()] = None,
) -> schema.InvoiceUpdate:
    return schema.InvoiceUpdate(
        attempt_count=attempt_count,
        attempted=attempted == "true",
        amount_paid=amount_paid,
        amount_remaining=amount_remaining,
        due_date=due_date,
    )
