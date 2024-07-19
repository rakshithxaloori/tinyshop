from pydantic import BaseModel

from lib.model import PyBaseModel
from lib.object import ObjectType
from invoice.model import InvoiceStatusEnum


class InvoiceCustomerAddress(BaseModel):
    line1: str
    line2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str


class InvoiceBase(BaseModel):
    amount_paid: int
    due_date: int
    status: InvoiceStatusEnum


class InvoiceCreate(InvoiceBase):
    checkout: str | None = None
    subscriptions: list[str] = []


class Invoice(InvoiceBase, PyBaseModel):
    id: str
    object: str = ObjectType.INVOICE
    amount_remaining: int
    amount_shipping: int
    amount_tax: int
    amount_subtotal: int
    amount_total: int
    amount_discount: int
    currency: str
    attempt_count: int
    attempted: bool
    invoice_pdf: str | None = None
    paid: bool
    customer: str
    checkout: str
    subscriptions: list[str] = []
    customer_address: InvoiceCustomerAddress


class InvoiceList(BaseModel):
    object: str = "list"
    data: list[Invoice] = []
    has_more: bool
    url: str = "/v1/invoices"


class InvoiceUpdate(BaseModel):
    attempt_count: int | None = None
    attempted: bool | None = None
    amount_paid: int | None = None
    amount_remaining: int | None = None
    due_date: int | None = None


class InvoiceDelete(BaseModel):
    id: str
    object: str = ObjectType.INVOICE
    deleted: bool
