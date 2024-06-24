from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel


from customer import schema, crud
from database import SessionLocal


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CustomerList(BaseModel):
    object: str = "list"
    url: str = "/v1/customers"
    has_more: bool
    data: list[schema.Customer] = []


@router.get("/customers", response_model=CustomerList)
def read_item(db: Session = Depends(get_db)):
    # new_customer: schemas.CustomerCreate = schemas.CustomerCreate(
    #     email="{}@gmail.com".format(get_primary_key("em", 10)()),
    #     password="{}".format(get_primary_key("em", 10)()),
    # )
    # crud.create_customer(db, new_customer)
    customers = crud.get_customers(db)
    print("Customers:", customers)

    return CustomerList(
        has_more=False,
        data=[customer.__dict__ for customer in customers],
    )
