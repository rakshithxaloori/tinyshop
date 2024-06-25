from fastapi import FastAPI, APIRouter


from team import model as team_models
from shop import model as shop_models
from customer import model as customer_models
from product import model as product_models
from product.option import model as option_models
from product.variant import model as variant_models
from product.price import model as price_models

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
