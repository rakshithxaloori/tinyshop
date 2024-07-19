from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends


from invoice import schema, crud, form
from lib.dependencies import ShopIDDep, LivemodeDep
from lib.session import get_session


router = APIRouter(prefix="/v1/invoices")


@router.post("", response_model=schema.Invoice)
def create_invoice(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    invoice: Annotated[schema.InvoiceCreate, Depends(form.create_invoice_form)],
    db: Session = Depends(get_session),
):
    new_invoice = crud.create_invoice(
        shop_id,
        livemode,
        invoice,
        db,
    )
    return new_invoice


@router.post("/{invoice_id}", response_model=schema.Invoice)
def update_invoice(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    invoice_id: str,
    invoice: Annotated[schema.InvoiceUpdate, Depends(form.update_invoice_form)],
    db: Session = Depends(get_session),
):
    updated_invoice = crud.update_invoice(
        shop_id,
        livemode,
        invoice_id,
        invoice,
        db,
    )
    return updated_invoice


@router.get("/{invoice_id}", response_model=schema.Invoice)
def retrieve_invoice(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    invoice_id: str,
    db: Session = Depends(get_session),
):
    invoice = crud.retrieve_invoice(
        shop_id,
        livemode,
        invoice_id,
        db,
    )
    return invoice


@router.get("", response_model=schema.InvoiceList)
def list_invoices(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    db: Session = Depends(get_session),
):
    # TODO skip, limit
    invoices_list = crud.list_invoices(
        shop_id,
        livemode,
        db,
    )
    return invoices_list


@router.delete("/{invoice_id}", response_model=schema.InvoiceDelete)
def delete_invoice(
    shop_id: ShopIDDep,
    livemode: LivemodeDep,
    invoice_id: str,
    db: Session = Depends(get_session),
):
    deleted_id = crud.delete_invoice(
        shop_id,
        livemode,
        invoice_id,
        db,
    )
    return schema.InvoiceDelete(
        id=invoice_id,
        deleted=deleted_id is not None,
    )
