import base64
from sqlmodel import SQLModel
from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import JSONResponse

import team.model as team_models
import shop.model as shop_models

import customer.model as customer_models
import customer.address.model as customer_address_models

from product import model as product_models
from product.option import model as option_models
from product.variant import model as variant_models
from product.price import model as price_models

from warehouse import model as warehouse_models
from warehouse.inventory import model as inventory_models

from cart import model as cart_models
from cart.cart_item import model as cart_item_models

# from discount import model as discount_models

from database import engine

from customer.router import router as customers_router
from customer.address.router import router as customer_addresses_router

from product.router import router as products_router
from product.option.router import router as options_router
from product.variant.router import router as variant_router
from product.price.router import router as price_router

from warehouse.router import router as warehouse_router
from warehouse.inventory.router import router as inventory_router

from cart.router import router as cart_router
from cart.cart_item.router import router as cart_item_router

from lib.dependencies import ShopIDDep, LivemodeDep

SQLModel.metadata.create_all(bind=engine)


app = FastAPI(root_path="tinyshop")


# TODO middleware to log your requests or cache the results


@app.middleware("http")
async def get_credentials(request: Request, call_next):
    # TODO if it's not a dashboard login route
    auth = request.headers.get("Authorization")
    scheme, data = (auth or " ").split(" ", 1)
    if scheme != "Basic":
        return JSONResponse(
            content={"message": "Only Basic Authentication is allowed"},
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    username, _ = base64.b64decode(data).decode().split(":", 1)
    secret_key = "sk_test_1234abcd"
    if username != secret_key:
        return JSONResponse(
            content={"message": "Secret key is invalid"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    livemode = username.split("_")[1]
    if livemode not in ["live", "test"]:
        return JSONResponse(
            content={"message": "Secret key is invalid"},
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    headers = dict(request.scope["headers"])
    headers[b"x-shop-id"] = str.encode(
        "shop_8hCaozNw3kSAfBaYCSTSNX"
    )  # TODO get shop id
    headers[b"x-livemode"] = str.encode(livemode)
    request.scope["headers"] = [(k, v) for k, v in headers.items()]
    response = await call_next(request)
    return response


# TODO delete main_router
main_router = APIRouter()


@main_router.get("/")
def read_root(x_shop_id: ShopIDDep, x_livemode: LivemodeDep):
    print(x_shop_id, x_livemode)
    return {"Hello": "World"}


app.include_router(main_router)
app.include_router(customers_router)
app.include_router(customer_addresses_router)

app.include_router(products_router)
app.include_router(options_router)
app.include_router(variant_router)
app.include_router(price_router)

app.include_router(warehouse_router)
app.include_router(inventory_router)

app.include_router(cart_router)
app.include_router(cart_item_router)
