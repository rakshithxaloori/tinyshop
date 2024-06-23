from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from .customers import schemas, crud, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
    data: list[schemas.Customer] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/customers", response_model=CustomerList)
def read_item(db: Session = Depends(get_db)):
    new_customer: schemas.CustomerCreate = schemas.CustomerCreate(
        email="{}@gmail.com".format(get_primary_key("em", 10)()),
        password="{}".format(get_primary_key("em", 10)()),
    )
    crud.create_customer(db, new_customer)
    customers = crud.get_customers(db)
    return CustomerList(
        has_more=False, data=[customer.__dict__ for customer in customers]
    )
