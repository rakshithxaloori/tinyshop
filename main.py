from fastapi import FastAPI, APIRouter


from team import models as team_models
from shop import models as shop_models
from customer import models as customer_models
from customer.addresses import models as address_models

from database import engine, Base
from utils.base import SqlBase
from customer.router import router as customers_router


Base.metadata.create_all(bind=engine)
SqlBase.metadata.create_all(bind=engine)

app = FastAPI()
main_router = APIRouter()


@main_router.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(main_router)
app.include_router(customers_router)
